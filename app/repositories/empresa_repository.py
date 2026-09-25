"""Repositorio específico para la entidad Empresa."""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.repositories.base_repository import RepositorioBase


class RepositorioEmpresa(RepositorioBase[Empresa]):
    """Acceso a datos para la entidad Empresa."""

    def __init__(self, db: Session) -> None:
        """Inicializa el repositorio asociado al modelo Empresa."""
        super().__init__(db, Empresa)

    def obtener_por_nombre(self, nombre: str) -> Optional[Empresa]:
        """Devuelve la empresa con el nombre indicado, o None si no existe."""
        return self.db.query(Empresa).filter(Empresa.nombre == nombre).first()