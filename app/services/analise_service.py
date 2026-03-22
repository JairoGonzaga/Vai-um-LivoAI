from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time
import asyncio
from typing import Any

from app.models.sessao import Sessao
from app.models.analise_yolo import AnaliseYolo
from app.models.recomendacao import Recomendacao
from app.schemas.sessao import SessaoResultado
from app.schemas.livro import LivroResponse
from app.schemas.recomendacao import RecomendacaoResponse
from app.services import storage_service, livro_service, yolo_service, ia_service, ocr_service
from app.core.security import gerar_token_sessao

logger = logging.getLogger("livroai.analise")
MAX_NOMES_PARA_ENRIQUECER = 8
MAX_RECOMENDACOES_PARA_SALVAR = 6
MAX_CONCORRENCIA_ENRIQUECIMENTO = 6


def _deduplicar_nomes(items: list[str]) -> list[str]:
    vistos = set()
    unicos = []

    for item in items:
        nome = str(item or "").strip()
        if not nome:
            continue

        chave = nome.lower()
        if chave in vistos:
            continue

        vistos.add(chave)
        unicos.append(nome)

    return unicos


async def _buscar_livro_com_limite(db: AsyncSession, nome: str, semaforo: asyncio.Semaphore):
    async with semaforo:
        return await livro_service.get_or_fetch(db, nome)


async def _enriquecer_livros_concorrente(db: AsyncSession, nomes: list[str]) -> list[Any]:
    if not nomes:
        return []

    semaforo = asyncio.Semaphore(MAX_CONCORRENCIA_ENRIQUECIMENTO)
    tarefas = [_buscar_livro_com_limite(db, nome, semaforo) for nome in nomes]
    resultados = await asyncio.gather(*tarefas, return_exceptions=True)

    livros = []
    for resultado in resultados:
        if isinstance(resultado, Exception):
            logger.warning("analise.livro_enriquecimento_falhou erro=%s", str(resultado))
            continue
        if resultado is not None:
            livros.append(resultado)

    return livros


async def _processar_recomendacao_com_limite(
    db: AsyncSession,
    sessao_id,
    rec: dict,
    semaforo: asyncio.Semaphore,
) -> tuple[Recomendacao, Any] | None:
    nome_recomendado = str(rec.get("nome", "")).strip()
    if not nome_recomendado:
        return None

    try:
        async with semaforo:
            livro = await livro_service.get_or_fetch(db, nome_recomendado)
    except Exception:
        return None

    if not livro:
        return None

    recomendacao = Recomendacao(
        sessao_id=sessao_id,
        livro_id=livro.id,
        justificativa_ia=rec.get("justificativa"),
        tipo_recomendacao=rec.get("tipo_recomendacao"),
    )
    return recomendacao, livro

async def processar(db: AsyncSession, foto: UploadFile) -> SessaoResultado:
    total_start = time.perf_counter()
    logger.info("analise.started filename=%s content_type=%s", foto.filename, foto.content_type)

    step_start = time.perf_counter()
    imagem_bytes = await foto.read()
    logger.info("analise.step arquivo_lido bytes=%s duration_ms=%s", len(imagem_bytes), int((time.perf_counter() - step_start) * 1000))

    step_start = time.perf_counter()
    resultado_yolo = await yolo_service.detectar(imagem_bytes, foto.content_type)
    bboxes = resultado_yolo.get("bboxes", [])
    logger.info("analise.step yolo_concluido bboxes=%s duration_ms=%s", len(bboxes), int((time.perf_counter() - step_start) * 1000))

    if not bboxes:
        raise HTTPException(
            status_code=422,
            detail="Nenhuma lombada detectada para OCR na imagem enviada.",
        )

    step_start = time.perf_counter()
    textos_ocr = await ocr_service.extrair_textos_segmentados(imagem_bytes, bboxes)
    logger.info("analise.step ocr_concluido textos=%s duration_ms=%s", len(textos_ocr), int((time.perf_counter() - step_start) * 1000))
    if not textos_ocr:
        raise HTTPException(
            status_code=422,
            detail="OCR não retornou texto válido. Verifique as credenciais do Google Vision e a qualidade da imagem.",
        )

    sessao = Sessao()
    db.add(sessao)
    await db.flush()  
    await db.refresh(sessao, attribute_names=["expira_em"])

    step_start = time.perf_counter()
    imagem_url = await storage_service.upload(foto, imagem_bytes)
    logger.info("analise.step upload_storage_concluido duration_ms=%s", int((time.perf_counter() - step_start) * 1000))
    entradas_ia = textos_ocr

    analise = AnaliseYolo(
        sessao_id=sessao.id,
        imagem_url=imagem_url,
        bboxes_json=bboxes,
        livros_detectados_json=entradas_ia,
        modelo_versao="1.0",
    )
    db.add(analise)

    step_start = time.perf_counter()
    nomes_limpos = _deduplicar_nomes(await ia_service.limpar_nomes(entradas_ia))
    nomes_base = nomes_limpos[:MAX_NOMES_PARA_ENRIQUECER]
    logger.info("analise.step limpeza_nomes_concluida nomes=%s duration_ms=%s", len(nomes_limpos), int((time.perf_counter() - step_start) * 1000))

    step_start = time.perf_counter()
    livros_encontrados = await _enriquecer_livros_concorrente(db, nomes_base)
    logger.info("analise.step livros_enriquecidos total=%s duration_ms=%s", len(livros_encontrados), int((time.perf_counter() - step_start) * 1000))

    step_start = time.perf_counter()
    recomendacoes_ia = await ia_service.gerar_recomendacoes(nomes_base)
    logger.info("analise.step recomendacoes_geradas total=%s duration_ms=%s", len(recomendacoes_ia), int((time.perf_counter() - step_start) * 1000))

    recomendacoes_salvas = []
    nomes_recomendados_processados = set()
    recomendacoes_pendentes: list[tuple[Recomendacao, Any]] = []
    recomendacoes_unicas = []

    for rec in recomendacoes_ia:
        if len(recomendacoes_unicas) >= MAX_RECOMENDACOES_PARA_SALVAR:
            break

        nome_recomendado = str(rec.get("nome", "")).strip()
        if not nome_recomendado:
            continue

        chave_nome_recomendado = nome_recomendado.lower()
        if chave_nome_recomendado in nomes_recomendados_processados:
            continue
        nomes_recomendados_processados.add(chave_nome_recomendado)
        recomendacoes_unicas.append(rec)

    semaforo_recomendacoes = asyncio.Semaphore(MAX_CONCORRENCIA_ENRIQUECIMENTO)
    tarefas_recomendacoes = [
        _processar_recomendacao_com_limite(db, sessao.id, rec, semaforo_recomendacoes)
        for rec in recomendacoes_unicas
    ]

    resultados_recomendacoes = await asyncio.gather(*tarefas_recomendacoes, return_exceptions=True)
    for resultado in resultados_recomendacoes:
        if isinstance(resultado, Exception) or resultado is None:
            continue
        recomendacao, livro = resultado
        db.add(recomendacao)
        recomendacoes_pendentes.append((recomendacao, livro))

    if recomendacoes_pendentes:
        await db.flush()

    for recomendacao, livro in recomendacoes_pendentes:
        recomendacoes_salvas.append(
            RecomendacaoResponse(
                id=recomendacao.id,
                sessao_id=recomendacao.sessao_id,
                livro_id=recomendacao.livro_id,
                justificativa_ia=recomendacao.justificativa_ia,
                tipo_recomendacao=recomendacao.tipo_recomendacao,
                data_geracao=recomendacao.data_geracao,
                livro=LivroResponse.model_validate(livro),
            )
        )

    await db.commit()

    logger.info(
        "analise.finished sessao_id=%s livros=%s recomendacoes=%s duration_ms=%s",
        sessao.id,
        len(livros_encontrados),
        len(recomendacoes_salvas),
        int((time.perf_counter() - total_start) * 1000),
    )

    return SessaoResultado(
        sessao_id=sessao.id,
        session_token=gerar_token_sessao(sessao.id, sessao.expira_em),
        livros_detectados=[LivroResponse.model_validate(l) for l in livros_encontrados],
        recomendacoes=recomendacoes_salvas,
    )