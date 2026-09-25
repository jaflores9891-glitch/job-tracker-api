"""Repositorio específico para la entidad Aplicacion."""
from sqlalchemy.orm import Session

from app.models.aplicacion import Aplicacion, EstatusAplicacion
from app.repositories.base_repository import RepositorioBase


class RepositorioAplicacion(RepositorioBase[Aplicacion]):
    """Acceso a datos para la entidad Aplicacion."""

    def __init__(self, db: Session) -> None:
        """Inicializa el repositorio asociado al modelo Aplicacion."""
        super().__init__(db, Aplicacion)

    def obtener_por_estatus(self, estatus: EstatusAplicacion) -> list[Aplicacion]:
        """Devuelve todas las aplicaciones con el estado indicado."""
        return self.db.query(Aplicacion).filter(Aplicacion.estatus == estatus).all()

    def obtener_por_vacante(self, vacante_id: int) -> list[Aplicacion]:
        """Devuelve todas las aplicaciones pertenecientes a la vacante indicada."""
        return self.db.query(Aplicacion).filter(Aplicacion.vacante_id == vacante_id).all()