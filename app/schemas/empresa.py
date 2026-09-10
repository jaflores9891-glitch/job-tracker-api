"""Schemas de Pydantic para la entidad Empresa."""
from pydantic import BaseModel, ConfigDict


class EmpresaBase(BaseModel):
    """Campos compartidos entre creación y respuesta."""

    nombre: str
    industria: str | None = None
    sitio_web: str | None = None


class EmpresaCreate(EmpresaBase):
    """Datos que el cliente envía al crear una empresa."""
    pass


class EmpresaUpdate(BaseModel):
    """Datos que el cliente puede enviar al actualizar una empresa.

    Todos los campos son opcionales: solo se actualizan los que se envíen.
    """

    nombre: str | None = None
    industria: str | None = None
    sitio_web: str | None = None


class EmpresaResponse(EmpresaBase):
    """Forma en que se devuelve una empresa al cliente."""

    model_config = ConfigDict(from_attributes=True)

    id: int