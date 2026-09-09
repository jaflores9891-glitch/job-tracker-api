"""Repositorio específico para la entidad Empresa."""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.repositories.base_repository import RepositorioBase


class RepositorioEmpresa(RepositorioBase[Empresa]):

    def __init__(self, db: Session) -> None:
        super().__init__(db, Empresa)

    def obtener_por_nombre(self, nombre: str) -> Optional[Empresa]:
        return self.db.query(Empresa).filter(Empresa.nombre == nombre).first()