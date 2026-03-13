# app/models/sessao.py

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.analise_yolo import AnaliseYolo
    from app.models.recomendacao import Recomendacao


class Sessao(Base):
    __tablename__ = "sessoes"

    id:        Mapped[uuid.UUID]  = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    criado_em: Mapped[datetime]   = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expira_em: Mapped[datetime]   = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now() + func.make_interval(hours=24))

    analises:      Mapped[List["AnaliseYolo"]]   = relationship(back_populates="sessao", cascade="all, delete-orphan")
    recomendacoes: Mapped[List["Recomendacao"]]  = relationship(back_populates="sessao", cascade="all, delete-orphan")