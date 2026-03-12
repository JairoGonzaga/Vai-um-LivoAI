from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

from app.schemas.livro import LivroResponse


class EstanteBase(BaseModel):
    status:         str        = "quero_ler"
    avaliacao:      int | None = None
    data_conclusao: datetime | None = None

class EstanteCreate(EstanteBase):
    user_id: UUID
    livro_id: UUID  


class EstanteResponse(EstanteBase):
    id: UUID
    user_id: UUID
    livro_id: UUID  
    data_adicao: date | None = None
    livro:       LivroResponse | None = None

    model_config = ConfigDict(from_attributes=True)