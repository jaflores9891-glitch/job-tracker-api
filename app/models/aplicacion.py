"""Modelo de la entidad Aplicacion."""
from datetime import date
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.vacante import Vacante


class EstatusAplicacion(str, PyEnum):
    """Posibles estatus de una aplicación a una vacante."""

    APLICADO = "aplicado"
    ENTREVISTA = "entrevista"
    OFERTA = "oferta"
    RECHAZADO = "rechazado"


class Aplicacion(Base):
    """Representa una aplicación enviada a una vacante.

    Attributes:
        id: Identificador único de la aplicación.
        vacante_id: Identificador de la vacante a la que se aplicó. Al
            eliminar la vacante, esta aplicación se elimina en cascada.
        fecha_aplicacion: Fecha en que se envió la aplicación.
        estatus: Estatus actual dentro del flujo aplicado → entrevista →
            oferta / rechazado.
        notas: Notas libres sobre la aplicación.
        vacante: La vacante a la que corresponde esta aplicación.
    """

    __tablename__ = "aplicaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    vacante_id: Mapped[int] = mapped_column(ForeignKey("vacantes.id", ondelete="CASCADE"), nullable=False)
    fecha_aplicacion: Mapped[date] = mapped_column(Date, nullable=False)
    estatus: Mapped[EstatusAplicacion] = mapped_column(
        Enum(EstatusAplicacion, name="estatus_aplicacion"),
        nullable=False,
        default=EstatusAplicacion.APLICADO,
    )
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    vacante: Mapped["Vacante"] = relationship()

    def __repr__(self) -> str:
        """Devuelve una representación legible de esta aplicación."""
        return f"<Aplicacion id={self.id} estatus={self.estatus.value!r}>"