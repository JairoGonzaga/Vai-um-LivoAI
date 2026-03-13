# app/schemas/recomendacao.py

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.livro import LivroResponse


class RecomendacaoBase(BaseModel):
    justificativa_ia:  str | None = None
    tipo_recomendacao: str | None = None


class RecomendacaoCreate(RecomendacaoBase):
    sessao_id: UUID
    livro_id:  UUID


class RecomendacaoResponse(RecomendacaoBase):
    id:           UUID
    sessao_id:    UUID
    livro_id:     UUID
    data_geracao: datetime
    livro:        LivroResponse | None = None

    model_config = ConfigDict(from_attributes=True)