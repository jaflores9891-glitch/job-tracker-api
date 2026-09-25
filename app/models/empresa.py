"""Modelo de la entidad Empresa."""
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, Relationship, mapped_column

from app.database import Base

if TYPE_CHECKING:
    from app.models.vacante import Vacante


class Empresa(Base):
    """Representa una empresa que publica vacantes de trabajo.

    Attributes:
        id: Identificador único de la empresa.
        nombre: Nombre de la empresa. Debe ser único en el sistema.
        industria: Sector o industria a la que pertenece la empresa.
        sitio_web: URL del sitio web de la empresa.
        vacantes: Vacantes publicadas por esta empresa. Al eliminar la
            empresa, estas vacantes se eliminan en cascada, junto con las
            aplicaciones asociadas a ellas.
    """

    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    industria: Mapped[str] = mapped_column(String(100), nullable=True)
    sitio_web: Mapped[str] = mapped_column(String(255), nullable=True)

    vacantes: Mapped[list["Vacante"]] = Relationship(
        back_populates="empresa", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Devuelve una representación legible de la empresa para desarrollo."""
        return f"<Empresa id={self.id} nombre={self.nombre!r}>"