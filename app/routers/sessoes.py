# app/routers/sessoes.py

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import extrair_token_sessao, validar_token_sessao
from app.schemas.sessao import SessaoResultado
from app.services import sessao_service

router = APIRouter()
settings = get_settings()


async def validar_acesso_sessao(
    sessao_id: UUID,
    authorization: str | None = Header(default=None),
    x_session_token: str | None = Header(default=None, alias="x-session-token"),
):
    segredo = (settings.SESSION_TOKEN_SECRET or "").strip()
    if not segredo:
        return

    token = extrair_token_sessao(authorization, x_session_token)
    if not token:
        raise HTTPException(status_code=401, detail="Token de sessão ausente")

    if not validar_token_sessao(token, sessao_id):
        raise HTTPException(status_code=403, detail="Token de sessão inválido")


@router.get("/{sessao_id}", response_model=SessaoResultado)
async def buscar_sessao(
    sessao_id: UUID,
    _: None = Depends(validar_acesso_sessao),
    db:        AsyncSession = Depends(get_db),
):
    sessao = await sessao_service.buscar(db, sessao_id)

    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada")

    return sessao


@router.get("/{sessao_id}/valida")
async def verificar_sessao(
    sessao_id: UUID,
    _: None = Depends(validar_acesso_sessao),
    db:        AsyncSession = Depends(get_db),
):
    valida = await sessao_service.verificar(db, sessao_id)

    return {"valida": valida}


@router.delete("/{sessao_id}", status_code=204)
async def deletar_sessao(
    sessao_id: UUID,
    _: None = Depends(validar_acesso_sessao),
    db:        AsyncSession = Depends(get_db),
):
    deletado = await sessao_service.deletar(db, sessao_id)

    if not deletado:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")