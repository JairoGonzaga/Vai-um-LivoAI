from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.users import users


class analise_yolo(Base):
    __tablename__ = "analise_yolo"

    id:                         Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id:                    Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    imagem_url:                 Mapped[str]         = mapped_column(Text, nullable=False)
    bboxes_json:                Mapped[Any | None]  = mapped_column(JSONB, nullable=True)
    livros_detectados_json:     Mapped[Any | None]  = mapped_column(JSONB, nullable=True)
    confirmado_pelo_usuario:    Mapped[bool]        = mapped_column(Boolean, nullable=False, server_default="false", index=True)
    usado_no_treino:            Mapped[bool]        = mapped_column(Boolean, nullable=False, server_default="false", index=True)
    modelo_versao:              Mapped[str | None]  = mapped_column(String(50), nullable=True)
    data_captura:               Mapped[datetime]    = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["users"] = relationship(back_populates="analise_yolo")