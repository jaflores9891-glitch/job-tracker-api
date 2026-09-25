"""Lógica de negocio para la entidad Aplicacion."""
import logging
from datetime import date

from sqlalchemy.orm import Session

from app.models.aplicacion import Aplicacion, EstatusAplicacion
from app.repositories.aplicacion_repository import RepositorioAplicacion
from app.services.exceptions import AplicacionNoEncontradaError, TransicionInvalidaError
from app.services.vacante_service import VacanteService

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
        """Inicializa el servicio con una sesión de base de datos."""
        self.repo = RepositorioAplicacion(db)
        self.vacante_service = VacanteService(db)

    def crear_aplicacion(self, vacante_id: int, fecha_aplicacion: date,
                          notas: str | None = None) -> Aplicacion:
        """Crea una nueva aplicación para una vacante existente.

        Raises:
            VacanteNoEncontradaError: Si no existe ninguna vacante con
                vacante_id.
        """
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
        """Devuelve la aplicación con el ID indicado.

        Raises:
            AplicacionNoEncontradaError: Si no existe ninguna aplicación
                con ese ID.
        """
        aplicacion = self.repo.obtener_por_id(aplicacion_id)
        if aplicacion is None:
            logger.warning("Aplicación no encontrada: id=%s", aplicacion_id)
            raise AplicacionNoEncontradaError(aplicacion_id)
        return aplicacion

    def cambiar_estatus(self, aplicacion_id: int,
                         nuevo_estatus: EstatusAplicacion) -> Aplicacion:
        """Cambia el estatus de una aplicación, validando la transición.

        Raises:
            AplicacionNoEncontradaError: Si no existe ninguna aplicación
                con ese ID.
            TransicionInvalidaError: Si la transición de estatus solicitada
                no está permitida por el flujo de negocio.
        """
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
        """Devuelve todas las aplicaciones con el estatus indicado."""
        return self.repo.obtener_por_estatus(estatus)

    def eliminar_aplicacion(self, aplicacion_id: int) -> None:
        """Elimina una aplicación existente."""
        self.obtener_aplicacion(aplicacion_id)
        self.repo.eliminar(aplicacion_id)

    def listar_aplicaciones_de_vacante(self, vacante_id: int) -> list[Aplicacion]:
        """Devuelve todas las aplicaciones de una vacante existente.

        Raises:
            VacanteNoEncontradaError: Si no existe ninguna vacante con
                vacante_id.
        """
        self.vacante_service.obtener_vacante(vacante_id)
        return self.repo.obtener_por_vacante(vacante_id)