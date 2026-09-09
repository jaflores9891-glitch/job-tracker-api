"""Repositorio específico para la entidad Aplicacion."""
from sqlalchemy.orm import Session

from app.models.aplicacion import Aplicacion, EstatusAplicacion
from app.repositories.base_repository import RepositorioBase


class RepositorioAplicacion(RepositorioBase[Aplicacion]):

    def __init__(self, db: Session) -> None:
        super().__init__(db, Aplicacion)

    def obtener_por_estatus(self, estatus: EstatusAplicacion) -> list[Aplicacion]:
        return self.db.query(Aplicacion).filter(Aplicacion.estatus == estatus).all()