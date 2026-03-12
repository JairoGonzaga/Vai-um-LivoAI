from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    nome:              str
    generos_favoritos: list[str] = []
    autores_favoritos: list[str] = []
    idioma_preferido:  str       = "pt-BR"


class UserCreate(UserBase):
    email:str

class UserUpdate(BaseModel):
    nome:              str | None = None
    generos_favoritos: list[str] | None = None
    autores_favoritos: list[str] | None = None
    idioma_preferido:  str | None = None

class UserResponse(UserBase):
    id:        UUID
    email:     str
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)