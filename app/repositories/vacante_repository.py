"""Repositorio específico para la entidad Vacante."""
from sqlalchemy.orm import Session

from app.models.vacante import Vacante
from app.repositories.base_repository import RepositorioBase


class RepositorioVacante(RepositorioBase[Vacante]):

    def __init__(self, db: Session) -> None:
        super().__init__(db, Vacante)

    def obtener_por_empresa(self, empresa_id: int) -> list[Vacante]:
        return self.db.query(Vacante).filter(Vacante.empresa_id == empresa_id).all()