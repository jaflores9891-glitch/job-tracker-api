"""Modelo  de la entidad empresa."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from app.database import Base

class Empresa(Base):

    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    industria: Mapped[str] = mapped_column(String(100), nullable=True)
    sitio_web: Mapped[str] = mapped_column(String(255), nullable=True)

    vacantes: Mapped[list["Vacante"]] = Relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Empresa id={self.id} nombre={self.nombre!r}>"