# app/schemas/sessao.py

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.livro import LivroResponse
from app.schemas.recomendacao import RecomendacaoResponse


class SessaoCreate(BaseModel):
    pass


class SessaoResponse(BaseModel):
    id:        UUID
    criado_em: datetime
    expira_em: datetime

    model_config = ConfigDict(from_attributes=True)


class SessaoResultado(BaseModel):
    sessao_id:         UUID
    livros_detectados: list[LivroResponse]
    recomendacoes:     list[RecomendacaoResponse]