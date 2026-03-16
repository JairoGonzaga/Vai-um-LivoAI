from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.sessao import Sessao
from app.schemas.sessao import SessaoResultado
from app.schemas.livro import LivroResponse
from app.schemas.recomendacao import RecomendacaoResponse


async def buscar(db: AsyncSession, sessao_id: UUID) -> SessaoResultado | None:
    result = await db.execute(
        select(Sessao)
        .where(Sessao.id == sessao_id)
        .where(Sessao.expira_em > datetime.now(timezone.utc))
        .options(
            selectinload(Sessao.recomendacoes).selectinload("livro")
        )
    )
    sessao = result.scalar_one_or_none()

    if not sessao:
        return None

    livros_detectados = [
        LivroResponse.model_validate(rec.livro)
        for rec in sessao.recomendacoes
        if rec.livro
    ]

    recomendacoes = [
        RecomendacaoResponse.model_validate(rec)
        for rec in sessao.recomendacoes
    ]

    return SessaoResultado(
        sessao_id=sessao.id,
        livros_detectados=livros_detectados,
        recomendacoes=recomendacoes,
    )


async def verificar(db: AsyncSession, sessao_id: UUID) -> bool:
    result = await db.execute(
        select(Sessao.id)
        .where(Sessao.id == sessao_id)
        .where(Sessao.expira_em > datetime.now(timezone.utc))
    )
    return result.scalar_one_or_none() is not None


async def deletar(db: AsyncSession, sessao_id: UUID) -> bool:
    result = await db.execute(
        select(Sessao).where(Sessao.id == sessao_id)
    )
    sessao = result.scalar_one_or_none()

    if not sessao:
        return False

    await db.delete(sessao)
    return True