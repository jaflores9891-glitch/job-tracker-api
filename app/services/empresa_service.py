"""Lógica de negocio para la entidad Empresa."""
import logging

from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.repositories.empresa_repository import RepositorioEmpresa
from app.services.exceptions import EmpresaNoEncontradaError, EmpresaDuplicadaError

logger = logging.getLogger(__name__)


class EmpresaService:

    def __init__(self, db: Session) -> None:
        self.repo = RepositorioEmpresa(db)

    def crear_empresa(self, nombre: str, industria: str | None = None,
                       sitio_web: str | None = None) -> Empresa: 
        
        existente = self.repo.obtener_por_nombre(nombre)
        
        if existente is not None:
            logger.warning("Intento de crear empresa duplicada: %s", nombre)
            raise EmpresaDuplicadaError(nombre)

        nueva_empresa = Empresa(nombre=nombre, industria=industria, sitio_web=sitio_web)
        creada = self.repo.crear(nueva_empresa)
        logger.info("Empresa creada: id=%s nombre=%s", creada.id, creada.nombre)
        return creada

    def obtener_empresa(self, empresa_id: int) -> Empresa:
        
        empresa = self.repo.obtener_por_id(empresa_id)
        if empresa is None:
            logger.warning("Empresa no encontrada: id=%s", empresa_id)
            raise EmpresaNoEncontradaError(empresa_id)
        return empresa

    def listar_empresas(self) -> list[Empresa]:
        return self.repo.obtener_todos()

    def actualizar_empresa(self, empresa_id: int, datos: dict) -> Empresa:
    
        empresa = self.obtener_empresa(empresa_id)  # ya valida existencia
        for campo, valor in datos.items():
            setattr(empresa, campo, valor)
        return self.repo.actualizar(empresa)


    def eliminar_empresa(self, empresa_id: int) -> None:
    
        self.obtener_empresa(empresa_id)  # valida que exista antes de intentar borrar
        self.repo.eliminar(empresa_id)