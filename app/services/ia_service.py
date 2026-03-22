import json
import httpx
import logging
import asyncio
import re

from app.core.config import get_settings

logger = logging.getLogger("livroai.ia")
settings = get_settings()


async def _chamar_mistral(prompt: str, temperature: float = 0.4) -> str:
    ultima_excecao = None

    async with httpx.AsyncClient() as client:
        for tentativa in range(1, 3):
            try:
                resposta = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "mistral-large-latest",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                    },
                    timeout=30,
                )
                resposta.raise_for_status()
                return resposta.json()["choices"][0]["message"]["content"]
            except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.HTTPError) as error:
                ultima_excecao = error

                status = getattr(getattr(error, "response", None), "status_code", None)
                logger.warning(
                    "ia.mistral_call_failed tentativa=%s status=%s erro=%s",
                    tentativa,
                    status,
                    str(error),
                )

                if tentativa < 2:
                    await asyncio.sleep(0.5)

    if ultima_excecao:
        raise ultima_excecao

    raise RuntimeError("Falha inesperada ao chamar Mistral")


def _extrair_json(texto: str, tipo: str = "lista") -> list:
    abre = "[" if tipo == "lista" else "{"
    fecha = "]" if tipo == "lista" else "}"

    texto_limpo = str(texto or "").strip()
    candidatos: list[tuple[str, str]] = [("raw", texto_limpo)]

    match_bloco = re.search(r"```(?:json)?\s*(.*?)\s*```", texto_limpo, flags=re.IGNORECASE | re.DOTALL)
    if match_bloco:
        candidatos.append(("fenced", match_bloco.group(1).strip()))

    vistos = set()
    for origem, candidato in candidatos:
        if not candidato or candidato in vistos:
            continue
        vistos.add(candidato)
        try:
            resultado = json.loads(candidato)
            if origem != "raw":
                logger.info("ia.json_parse_recovered origem=%s", origem)
            return resultado
        except json.JSONDecodeError:
            inicio = candidato.find(abre)
            fim = candidato.rfind(fecha) + 1
            if inicio != -1 and fim > inicio:
                trecho = candidato[inicio:fim]
                if trecho in vistos:
                    continue
                vistos.add(trecho)
                try:
                    resultado = json.loads(trecho)
                    logger.info("ia.json_parse_recovered origem=%s intervalo=%s-%s", origem, inicio, fim)
                    return resultado
                except json.JSONDecodeError:
                    continue

    logger.warning("ia.json_parse_failed tipo=%s texto=%s", tipo, texto_limpo[:500])
    return []


async def limpar_nomes(nomes_brutos: list[str]) -> list[str]:
    if not nomes_brutos:
        logger.info("ia.limpar_nomes entrada vazia")
        return []

    logger.info("ia.limpar_nomes iniciando com %s nomes", len(nomes_brutos))
    logger.debug("ia.limpar_nomes nomes recebidos: %s", nomes_brutos)

    prompt = f"""Você recebeu os seguintes textos extraídos por OCR de capas de livros.
Eles podem conter erros de digitação, caracteres errados, fragmentos e ruídos:
{json.dumps(nomes_brutos, ensure_ascii=False)}

Sua tarefa:
1. Identificar quais são títulos reais de livros
2. Corrigir erros de OCR (ex: \"HOBB1T\" → \"O Hobbit\", \"198 Orwell\" → \"1984\")
3. Completar títulos fragmentados quando possível (ex: \"SENHOR DOS ANE\" → \"O Senhor dos Anéis\")
4. Ignorar textos que claramente não são títulos de livros
5. Responder apenas com uma lista JSON dos títulos corrigidos, sem explicações ou texto adicional.
6. Se não conseguir identificar nenhum título válido, responda com uma lista vazia: [].

Responda APENAS com JSON válido, sem texto antes ou depois, sem markdown, sem backticks:
[\"Título Correto 1\", \"Título Correto 2\"]"""

    try:
        texto = await _chamar_mistral(prompt, temperature=0.1)
        logger.debug("ia.limpar_nomes resposta IA (primeiros 1000 chars): %s", texto[:1000])

        resultado = _extrair_json(texto, tipo="lista")
        logger.info("ia.limpar_nomes completado com %s nomes após parsing", len(resultado))
        return resultado
    except Exception as error:
        logger.error("ia.limpar_nomes fallback por indisponibilidade da IA: %s", str(error))

        fallback = [str(item or "").strip() for item in nomes_brutos if str(item or "").strip()]
        logger.info("ia.limpar_nomes usando fallback com %s nomes", len(fallback))
        return fallback


async def gerar_recomendacoes(livros_detectados: list[str]) -> list[dict]:
    if not livros_detectados:
        return []

    prompt = f"""Você é um especialista em literatura.
Com base nos seguintes livros encontrados na estante do usuário:
{json.dumps(livros_detectados, ensure_ascii=False)}

Gere até 6 recomendações de livros que o usuário pode gostar.
Considere o gênero, autor e tema dos livros da estante para fazer recomendações relevantes.
Responda APENAS com JSON válido, sem texto antes ou depois, sem markdown, sem backticks:
[
  {{
    \"nome\": \"Nome do Livro\",
    \"autor\": \"Nome do Autor\",
    \"justificativa\": \"Motivo da recomendação baseado nos livros da estante\",
    \"tipo_recomendacao\": \"por_genero\"
  }}
]

Tipos válidos para tipo_recomendacao: por_genero, por_autor, por_tema, similar"""

    try:
        texto = await _chamar_mistral(prompt, temperature=0.7)
        return _extrair_json(texto, tipo="lista")
    except Exception as error:
        logger.error("ia.gerar_recomendacoes indisponível, retornando vazio: %s", str(error))
        return []
