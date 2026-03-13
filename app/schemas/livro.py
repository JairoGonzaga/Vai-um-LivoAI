from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
 
 
class LivroBase(BaseModel):
    nome:           str
    autor:          str
    genero:         str | None = None
    isbn:           str | None = None
    link:           str | None = None
    capa_url:       str | None = None
    sinopse:        str | None = None
    ano_publicacao: int | None = None
    editora:        str | None = None
 
 
class LivroCreate(LivroBase):
    pass
 
 
class LivroResponse(LivroBase):
    id:        UUID
    criado_em: datetime
 
    model_config = ConfigDict(from_attributes=True)