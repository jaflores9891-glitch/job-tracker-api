"""Lógica de negocio para la entidad Vacante."""
import logging
from datetime import date

from sqlalchemy.orm import Session

from app.models.vacante import Vacante
from app.repositories.vacante_repository import RepositorioVacante
from app.services.empresa_service import EmpresaService
from app.services.exceptions import VacanteNoEncontradaError

logger = logging.getLogger(__name__)


class VacanteService:
    """Encapsula las reglas de negocio relacionadas con vacantes."""

    def __init__(self, db: Session) -> None:

        self.repo = RepositorioVacante(db)
        self.empresa_service = EmpresaService(db)

    def crear_vacante(self, titulo: str, empresa_id: int,
                       salario_estimado: int | None = None,
                       modalidad: str | None = None,
                       tecnologias: list[str] | None = None,
                       fecha_publicacion: date | None = None) -> Vacante:
        
        self.empresa_service.obtener_empresa(empresa_id)

        nueva_vacante = Vacante(
            titulo=titulo,
            empresa_id=empresa_id,
            salario_estimado=salario_estimado,
            modalidad=modalidad,
            tecnologias=tecnologias,
            fecha_publicacion=fecha_publicacion,
        )
        creada = self.repo.crear(nueva_vacante)
        logger.info("Vacante creada: id=%s titulo=%s empresa_id=%s",
                    creada.id, creada.titulo, empresa_id)
        return creada

    def obtener_vacante(self, vacante_id: int) -> Vacante:

        vacante = self.repo.obtener_por_id(vacante_id)
        if vacante is None:
            logger.warning("Vacante no encontrada: id=%s", vacante_id)
            raise VacanteNoEncontradaError(vacante_id)
        return vacante

    def listar_vacantes_de_empresa(self, empresa_id: int) -> list[Vacante]:
       
        self.empresa_service.obtener_empresa(empresa_id)
        return self.repo.obtener_por_empresa(empresa_id)