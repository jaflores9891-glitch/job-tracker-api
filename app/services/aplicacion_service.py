"""Lógica de negocio para la entidad Aplicacion."""
import logging
from datetime import date

from sqlalchemy.orm import Session

from app.models.aplicacion import Aplicacion, EstatusAplicacion
from app.repositories.aplicacion_repository import RepositorioAplicacion
from app.services.vacante_service import VacanteService
from app.services.exceptions import AplicacionNoEncontradaError, TransicionInvalidaError

logger = logging.getLogger(__name__)

TRANSICIONES_VALIDAS: dict[EstatusAplicacion, set[EstatusAplicacion]] = {
    EstatusAplicacion.APLICADO: {EstatusAplicacion.ENTREVISTA, EstatusAplicacion.RECHAZADO},
    EstatusAplicacion.ENTREVISTA: {EstatusAplicacion.OFERTA, EstatusAplicacion.RECHAZADO},
    EstatusAplicacion.OFERTA: set(),
    EstatusAplicacion.RECHAZADO: set(),
}


class AplicacionService:
    """Encapsula las reglas de negocio relacionadas con aplicaciones."""

    def __init__(self, db: Session) -> None:

        self.repo = RepositorioAplicacion(db)
        self.vacante_service = VacanteService(db)

    def crear_aplicacion(self, vacante_id: int, fecha_aplicacion: date,
                          notas: str | None = None) -> Aplicacion:

        self.vacante_service.obtener_vacante(vacante_id)

        nueva = Aplicacion(
            vacante_id=vacante_id,
            fecha_aplicacion=fecha_aplicacion,
            notas=notas,
        )
        creada = self.repo.crear(nueva)
        logger.info("Aplicación creada: id=%s vacante_id=%s", creada.id, vacante_id)
        return creada

    def obtener_aplicacion(self, aplicacion_id: int) -> Aplicacion:

        aplicacion = self.repo.obtener_por_id(aplicacion_id)
        if aplicacion is None:
            logger.warning("Aplicación no encontrada: id=%s", aplicacion_id)
            raise AplicacionNoEncontradaError(aplicacion_id)
        return aplicacion

    def cambiar_estatus(self, aplicacion_id: int,
                         nuevo_estatus: EstatusAplicacion) -> Aplicacion:

        aplicacion = self.obtener_aplicacion(aplicacion_id)
        estatus_actual = aplicacion.estatus

        transiciones_permitidas = TRANSICIONES_VALIDAS[estatus_actual]
        if nuevo_estatus not in transiciones_permitidas:
            logger.warning(
                "Transición inválida en aplicación id=%s: %s -> %s",
                aplicacion_id, estatus_actual.value, nuevo_estatus.value,
            )
            raise TransicionInvalidaError(estatus_actual.value, nuevo_estatus.value)

        aplicacion.estatus = nuevo_estatus
        actualizada = self.repo.actualizar(aplicacion)
        logger.info(
            "Estatus actualizado: id=%s %s -> %s",
            aplicacion_id, estatus_actual.value, nuevo_estatus.value,
        )
        return actualizada

    def listar_por_estatus(self, estatus: EstatusAplicacion) -> list[Aplicacion]:

        return self.repo.obtener_por_estatus(estatus)