from __future__ import annotations
 
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List
 
from sqlalchemy import String, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
 
from app.core.database import Base
 
if TYPE_CHECKING:
    from app.models.estante import estantes
    from app.models.recomendacao import recomendacoes
    from app.models.analise_yolo import analise_yolo
 
 
class users(Base):
    __tablename__ = "users"
 
    id:                 Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    nome:               Mapped[str]         = mapped_column(String(150), nullable=False)
    email:              Mapped[str]         = mapped_column(String(255), nullable=False, unique=True, index=True)
    generos_favoritos:  Mapped[list]        = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    autores_favoritos:  Mapped[list]        = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    idioma_preferido:   Mapped[str]         = mapped_column(String(10),  nullable=False, server_default="pt-BR")
    criado_em:          Mapped[datetime]    = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    atualizado_em:      Mapped[datetime]    = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
 
    estante:        Mapped[List["estantes"]]      = relationship(back_populates="users")
    recomendacoes:  Mapped[List["recomendacoes"]] = relationship(back_populates="users")
    analises:       Mapped[List["analise_yolo"]]  = relationship(back_populates="users")
 