from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sessao import Sessao
from app.models.analise_yolo import AnaliseYolo
from app.models.recomendacao import Recomendacao
from app.schemas.sessao import SessaoResultado
from app.schemas.livro import LivroResponse
from app.schemas.recomendacao import RecomendacaoResponse
from app.services import storage_service, livro_service, yolo_service, ia_service, ocr_service

async def processar(db: AsyncSession, foto: UploadFile) -> SessaoResultado:

    imagem_bytes = await foto.read()

    sessao = Sessao()
    db.add(sessao)
    await db.flush()  

    imagem_url = await storage_service.upload(foto, imagem_bytes)

    resultado_yolo = await yolo_service.detectar(imagem_bytes, foto.content_type)
    nomes_brutos   = resultado_yolo.get("nomes_detectados", [])
    bboxes         = resultado_yolo.get("bboxes", [])
    textos_ocr     = await ocr_service.extrair_textos_segmentados(imagem_bytes, bboxes)

    entradas_ia = textos_ocr if textos_ocr else nomes_brutos

    analise = AnaliseYolo(
        sessao_id=sessao.id,
        imagem_url=imagem_url,
        bboxes_json=bboxes,
        livros_detectados_json=entradas_ia,
        modelo_versao="1.0",
    )
    db.add(analise)

    nomes_limpos = await ia_service.limpar_nomes(entradas_ia)

    livros_encontrados = []
    for nome in nomes_limpos:
        livro = await livro_service.get_or_fetch(db, nome)
        if livro is not None:
            livros_encontrados.append(livro)
    recomendacoes_ia = await ia_service.gerar_recomendacoes(nomes_limpos)

    recomendacoes_salvas = []

    for rec in recomendacoes_ia:
        nome_recomendado = str(rec.get("nome", "")).strip()
        if not nome_recomendado:
            continue

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
        await db.flush()

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

    return SessaoResultado(
        sessao_id=sessao.id,
        livros_detectados=[LivroResponse.model_validate(l) for l in livros_encontrados],
        recomendacoes=recomendacoes_salvas,
    )