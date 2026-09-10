"""Schemas de Pydantic para la entidad Aplicacion."""
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.aplicacion import EstatusAplicacion


class AplicacionBase(BaseModel):
    """Campos compartidos entre creación y respuesta."""

    vacante_id: int
    fecha_aplicacion: date
    notas: str | None = None


class AplicacionCreate(AplicacionBase):
    """Datos que el cliente envía al crear una aplicación."""
    pass


class CambioEstatusRequest(BaseModel):
    """Datos para solicitar un cambio de estatus."""

    nuevo_estatus: EstatusAplicacion


class AplicacionResponse(AplicacionBase):
    """Forma en que se devuelve una aplicación al cliente."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    estatus: EstatusAplicacion