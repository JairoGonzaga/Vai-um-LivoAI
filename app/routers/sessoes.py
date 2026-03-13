# app/routers/sessoes.py

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.sessao import SessaoResultado
from app.services import sessao_service

router = APIRouter()


@router.get("/{sessao_id}", response_model=SessaoResultado)
async def buscar_sessao(
    sessao_id: UUID,
    db:        AsyncSession = Depends(get_db),
):
    sessao = await sessao_service.buscar(db, sessao_id)

    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada")

    return sessao


@router.get("/{sessao_id}/valida")
async def verificar_sessao(
    sessao_id: UUID,
    db:        AsyncSession = Depends(get_db),
):
    valida = await sessao_service.verificar(db, sessao_id)

    return {"valida": valida}


@router.delete("/{sessao_id}", status_code=204)
async def deletar_sessao(
    sessao_id: UUID,
    db:        AsyncSession = Depends(get_db),
):
    deletado = await sessao_service.deletar(db, sessao_id)

    if not deletado:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")