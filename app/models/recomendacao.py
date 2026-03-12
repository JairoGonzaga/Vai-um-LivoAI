import uuid
from typing import TYPE_CHECKING
 
from sqlalchemy import String, SmallInteger, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
 
from app.core.database import Base
 
if TYPE_CHECKING:
    from app.models.users import users
    from app.models.livro import livros
 
 
class recomendacoes(Base):
    __tablename__ = "recomendacoes"
 
    id:                 Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id:            Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("users.id",  ondelete="CASCADE"),  nullable=False, index=True)
    livro_id:           Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("livros.id", ondelete="RESTRICT"), nullable=False)
    justificativa_ia:   Mapped[str | None]  = mapped_column(Text,        nullable=True)
    tipo_recomendacao:  Mapped[str | None]  = mapped_column(String(50),  nullable=True)
    status:             Mapped[str]         = mapped_column(String,      nullable=False, server_default="pendente", index=True)
    feedback:           Mapped[int | None]  = mapped_column(SmallInteger, nullable=True)
    data_geracao:       Mapped[DateTime]    = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
 
    user:  Mapped["users"]  = relationship(back_populates="recomendacoes")
    livro: Mapped["livros"] = relationship(back_populates="recomendacoes")
