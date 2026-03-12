from __future__ import annotations
 
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List
 
from sqlalchemy import String, Text, SmallInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
 
from app.core.database import Base
 
if TYPE_CHECKING:
    from app.models.estante import estantes
    from app.models.recomendacao import recomendacoes

class livros(Base):
    __tablename__ = "livros"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    autor:          Mapped[str]           = mapped_column(String(255), nullable=False, index=True)
    genero:         Mapped[str | None]    = mapped_column(String(100), nullable=True,  index=True)
    isbn:           Mapped[str | None]    = mapped_column(String(20),  nullable=True,  unique=True, index=True)
    link:           Mapped[str | None]    = mapped_column(Text,        nullable=True)
    capa_url:       Mapped[str | None]    = mapped_column(Text,        nullable=True)
    sinopse:        Mapped[str | None]    = mapped_column(Text,        nullable=True)
    ano_publicacao: Mapped[int | None]    = mapped_column(SmallInteger, nullable=True)
    editora:        Mapped[str | None]    = mapped_column(String(150), nullable=True)
    criado_em:      Mapped[DateTime]      = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
    estante:        Mapped[list["estantes"]]        = relationship(back_populates="livros")
    recomendacoes:  Mapped[list["recomendacoes"]]   = relationship(back_populates="livros")