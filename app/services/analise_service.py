from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time
import secrets
from typing import Any

from app.models.sessao import Sessao
from app.models.analise_yolo import AnaliseYolo
from app.models.recomendacao import Recomendacao
from app.schemas.sessao import SessaoResultado
from app.schemas.livro import LivroResponse
from app.schemas.recomendacao import RecomendacaoResponse
from app.services import storage_service, livro_service, yolo_service, ia_service, ocr_service

logger = logging.getLogger("livroai.analise")
MAX_NOMES_PARA_ENRIQUECER = 8
MAX_RECOMENDACOES_PARA_SALVAR = 6


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

    sessao = Sessao(token=secrets.token_hex(32))
    db.add(sessao)
    await db.flush()  

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
    livros_encontrados = []
    for nome in nomes_base:
        livro = await livro_service.get_or_fetch(db, nome)
        if livro is not None:
            livros_encontrados.append(livro)
    logger.info("analise.step livros_enriquecidos total=%s duration_ms=%s", len(livros_encontrados), int((time.perf_counter() - step_start) * 1000))

    step_start = time.perf_counter()
    recomendacoes_ia = await ia_service.gerar_recomendacoes(nomes_base)
    logger.info("analise.step recomendacoes_geradas total=%s duration_ms=%s", len(recomendacoes_ia), int((time.perf_counter() - step_start) * 1000))

    recomendacoes_salvas = []
    nomes_recomendados_processados = set()
    recomendacoes_pendentes: list[tuple[Recomendacao, Any]] = []

    for rec in recomendacoes_ia:
        if len(recomendacoes_pendentes) >= MAX_RECOMENDACOES_PARA_SALVAR:
            break

        nome_recomendado = str(rec.get("nome", "")).strip()
        if not nome_recomendado:
            continue

        chave_nome_recomendado = nome_recomendado.lower()
        if chave_nome_recomendado in nomes_recomendados_processados:
            continue
        nomes_recomendados_processados.add(chave_nome_recomendado)

        try:
            livro = await livro_service.get_or_fetch(db, nome_recomendado)
        except Exception:
            continue

        if not livro:
            continue

        recomendacao = Recomendacao(
            sessao_id=sessao.id,
            livro_id=livro.id,
            justificativa_ia=rec.get("justificativa"),
            tipo_recomendacao=rec.get("tipo_recomendacao"),
        )
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
        token=sessao.token,
        livros_detectados=[LivroResponse.model_validate(l) for l in livros_encontrados],
        recomendacoes=recomendacoes_salvas,
    )