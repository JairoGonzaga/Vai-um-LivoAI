import json
import httpx

from app.core.config import get_settings

settings = get_settings()


async def _chamar_mistral(prompt: str, temperature: float = 0.4) -> str:
    async with httpx.AsyncClient() as client:
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


def _extrair_json(texto: str, tipo: str = "lista") -> list:
    abre = "[" if tipo == "lista" else "{"
    fecha = "]" if tipo == "lista" else "}"
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        inicio = texto.find(abre)
        fim = texto.rfind(fecha) + 1
        if inicio != -1 and fim > inicio:
            return json.loads(texto[inicio:fim])
        return []


async def limpar_nomes(nomes_brutos: list[str]) -> list[str]:
    if not nomes_brutos:
        return []

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

    texto = await _chamar_mistral(prompt, temperature=0.1)
    return _extrair_json(texto, tipo="lista")


async def gerar_recomendacoes(livros_detectados: list[str]) -> list[dict]:
    if not livros_detectados:
        return []

    prompt = f"""Você é um especialista em literatura.
Com base nos seguintes livros encontrados na estante do usuário:
{json.dumps(livros_detectados, ensure_ascii=False)}

Gere exatamente 10 recomendações de livros que o usuário pode gostar.
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

    texto = await _chamar_mistral(prompt, temperature=0.7)
    return _extrair_json(texto, tipo="lista")
