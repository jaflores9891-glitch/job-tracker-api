"""Modelo de la entidad Aplicacion."""
from datetime import date
from enum import Enum as PyEnum

from sqlalchemy import Date, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EstatusAplicacion(str, PyEnum):
    """Posibles estatus de una aplicación a una vacante."""

    APLICADO = "aplicado"
    ENTREVISTA = "entrevista"
    OFERTA = "oferta"
    RECHAZADO = "rechazado"


class Aplicacion(Base):

    __tablename__ = "aplicaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    vacante_id: Mapped[int] = mapped_column(ForeignKey("vacantes.id"), nullable=False)
    fecha_aplicacion: Mapped[date] = mapped_column(Date, nullable=False)
    estatus: Mapped[EstatusAplicacion] = mapped_column(
        Enum(EstatusAplicacion, name="estatus_aplicacion"),
        nullable=False,
        default=EstatusAplicacion.APLICADO,
    )
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    vacante: Mapped["Vacante"] = relationship()

    def __repr__(self) -> str:
        return f"<Aplicacion id={self.id} estatus={self.estatus.value!r}>"

