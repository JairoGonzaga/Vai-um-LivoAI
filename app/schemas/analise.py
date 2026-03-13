# app/schemas/analise.py

from uuid import UUID
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class AnaliseCreate(BaseModel):
    sessao_id:              UUID
    imagem_url:             str
    bboxes_json:            Any | None = None
    livros_detectados_json: Any | None = None
    modelo_versao:          str | None = None


class AnaliseResponse(AnaliseCreate):
    id:                      UUID
    confirmado_pelo_usuario: bool
    usado_no_treino:         bool
    data_captura:            datetime

    model_config = ConfigDict(from_attributes=True)