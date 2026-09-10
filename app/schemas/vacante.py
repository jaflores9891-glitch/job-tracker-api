"""Schemas de Pydantic para la entidad Vacante."""
from datetime import date

from pydantic import BaseModel, ConfigDict


class VacanteBase(BaseModel):
    """Campos compartidos entre creación y respuesta."""

    titulo: str
    empresa_id: int
    salario_estimado: int | None = None
    modalidad: str | None = None
    tecnologias: list[str] | None = None
    fecha_publicacion: date | None = None


class VacanteCreate(VacanteBase):
    """Datos que el cliente envía al crear una vacante."""
    pass


class VacanteUpdate(BaseModel):
    """Datos que el cliente puede enviar al actualizar una vacante."""

    titulo: str | None = None
    salario_estimado: int | None = None
    modalidad: str | None = None
    tecnologias: list[str] | None = None
    fecha_publicacion: date | None = None


class VacanteResponse(VacanteBase):
    """Forma en que se devuelve una vacante al cliente."""

    model_config = ConfigDict(from_attributes=True)

    id: int