"""Modelo de la entidad Vacante."""
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa


class Vacante(Base):
    """Representa una vacante publicada por una empresa.

    Attributes:
        id: Identificador único de la vacante.
        titulo: Título del puesto.
        empresa_id: Identificador de la empresa que publicó la vacante.
        salario_estimado: Salario estimado ofrecido para la vacante.
        modalidad: Modalidad de trabajo (por ejemplo, remoto, presencial).
        tecnologias: Lista de tecnologías requeridas para el puesto.
        fecha_publicacion: Fecha en que se publicó la vacante.
        empresa: La empresa que publicó esta vacante.
    """

    __tablename__ = "vacantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    salario_estimado: Mapped[int] = mapped_column(Integer, nullable=True)
    modalidad: Mapped[str] = mapped_column(String(20), nullable=True)
    tecnologias: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    fecha_publicacion: Mapped[date] = mapped_column(Date, nullable=True)

    empresa: Mapped["Empresa"] = relationship(back_populates="vacantes")

    def __repr__(self) -> str:
        """Devuelve una representación legible de la vacante para desarrollo.."""
        return f"<Vacante id={self.id} titulo={self.titulo!r}>"