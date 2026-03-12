from __future__ import annotations
 
import uuid
from datetime import datetime, date
from typing import TYPE_CHECKING
 
from sqlalchemy import String, SmallInteger, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
 
from app.core.database import Base
 
if TYPE_CHECKING:
    from app.models.users import users
    from app.models.livro import livros
 
 
class estantes(Base):
    __tablename__ = "estantes"
 
    id:             Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id:        Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("users.id",  ondelete="CASCADE"),  nullable=False, index=True)
    livro_id:       Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("livros.id", ondelete="RESTRICT"), nullable=False, index=True)
    status:         Mapped[str]         = mapped_column(String,      nullable=False, server_default="quero_ler", index=True)
    avaliacao:      Mapped[int | None]  = mapped_column(SmallInteger, nullable=True)
    data_adicao:    Mapped[datetime]    = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_conclusao: Mapped[date | None] = mapped_column(Date, nullable=True)
 
    user:  Mapped["users"]  = relationship(back_populates="estantes")
    livro: Mapped["livros"] = relationship(back_populates="estantes")
 