"""Lógica de negocio para la entidad Empresa."""
import logging

from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.repositories.empresa_repository import RepositorioEmpresa
from app.services.exceptions import EmpresaDuplicadaError, EmpresaNoEncontradaError

logger = logging.getLogger(__name__)


class EmpresaService:
    """Encapsula las reglas de negocio relacionadas con empresas."""

    def __init__(self, db: Session) -> None:
        """Inicializa el servicio con una sesión de base de datos."""
        self.repo = RepositorioEmpresa(db)

    def crear_empresa(self, nombre: str, industria: str | None = None,
                       sitio_web: str | None = None) -> Empresa:
        """Crea una nueva empresa, rechazando nombres duplicados.

        Raises:
            EmpresaDuplicadaError: Si ya existe una empresa con el mismo
                nombre.
        """
        existente = self.repo.obtener_por_nombre(nombre)

        if existente is not None:
            logger.warning("Intento de crear empresa duplicada: %s", nombre)
            raise EmpresaDuplicadaError(nombre)

        nueva_empresa = Empresa(nombre=nombre, industria=industria, sitio_web=sitio_web)
        creada = self.repo.crear(nueva_empresa)
        logger.info("Empresa creada: id=%s nombre=%s", creada.id, creada.nombre)
        return creada

    def obtener_empresa(self, empresa_id: int) -> Empresa:
        """Devuelve la empresa con el ID indicado.

        Raises:
            EmpresaNoEncontradaError: Si no existe ninguna empresa con ese ID.
        """
        empresa = self.repo.obtener_por_id(empresa_id)
        if empresa is None:
            logger.warning("Empresa no encontrada: id=%s", empresa_id)
            raise EmpresaNoEncontradaError(empresa_id)
        return empresa

    def listar_empresas(self) -> list[Empresa]:
        """Devuelve todas las empresas registradas."""
        return self.repo.obtener_todos()

    def actualizar_empresa(self, empresa_id: int, datos: dict) -> Empresa:
        """Actualiza los campos indicados de una empresa existente."""
        empresa = self.obtener_empresa(empresa_id)  # ya valida existencia
        for campo, valor in datos.items():
            setattr(empresa, campo, valor)
        return self.repo.actualizar(empresa)

    def eliminar_empresa(self, empresa_id: int) -> None:
        """Elimina una empresa existente."""
        self.obtener_empresa(empresa_id)  # valida que exista antes de intentar borrar
        self.repo.eliminar(empresa_id)