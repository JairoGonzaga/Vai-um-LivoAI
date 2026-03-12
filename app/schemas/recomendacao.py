from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class RecomendacaoBase(BaseModel):
    justificativa_ia:str | None = None
    tipo_recomendacao: str | None = None
    status:str = "pendente"


class RecomendacaoCreate(RecomendacaoBase):
    user_id: UUID
    livro_id: UUID  

class RecomendacaoUpdate(BaseModel):
    status: str | None = None
    feedback: int | None = None

class RecomendacaoResponse(RecomendacaoBase):
    id:        UUID
    user_id: UUID
    livro_id: UUID  
    data_geracao: datetime
    feedback: int | None = None

    model_config = ConfigDict(from_attributes=True)