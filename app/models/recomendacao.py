
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.sessao import Sessao
    from app.models.livro import Livro


class Recomendacao(Base):
    __tablename__ = "recomendacoes"
    id:                 Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    sessao_id:          Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("sessoes.id",  ondelete="CASCADE"),  nullable=False, index=True)
    livro_id:           Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("livros.id",   ondelete="RESTRICT"), nullable=False, index=True)
    justificativa_ia:   Mapped[str | None]  = mapped_column(Text,        nullable=True)
    tipo_recomendacao:  Mapped[str | None]  = mapped_column(String(50),  nullable=True)
    data_geracao:       Mapped[datetime]    = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    sessao: Mapped["Sessao"] = relationship(back_populates="recomendacoes")
    livro:  Mapped["Livro"]  = relationship(back_populates="recomendacoes")