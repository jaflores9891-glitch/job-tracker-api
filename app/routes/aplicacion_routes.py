"""Rutas HTTP para la entidad Aplicacion."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aplicacion import EstatusAplicacion
from app.schemas.aplicacion import AplicacionCreate, AplicacionResponse, CambioEstatusRequest
from app.services.aplicacion_service import AplicacionService

router = APIRouter(prefix="/aplicaciones", tags=["Aplicaciones"])


@router.post("/", response_model=AplicacionResponse, status_code=201)
def crear_aplicacion(
    datos: AplicacionCreate,
    db: Session = Depends(get_db),
) -> AplicacionResponse:
    service = AplicacionService(db)
    return service.crear_aplicacion(**datos.model_dump())

@router.get("/vacante/{vacante_id}", response_model=list[AplicacionResponse])
def listar_aplicaciones_de_vacante(
    vacante_id: int,
    db: Session = Depends(get_db),
) -> list[AplicacionResponse]:
    service = AplicacionService(db)
    return service.listar_aplicaciones_de_vacante(vacante_id)

@router.get("/", response_model=list[AplicacionResponse])
def listar_por_estatus(
    estatus: EstatusAplicacion,
    db: Session = Depends(get_db),
) -> list[AplicacionResponse]:
    service = AplicacionService(db)
    return service.listar_por_estatus(estatus)

@router.get("/{aplicacion_id}", response_model=AplicacionResponse)
def obtener_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
) -> AplicacionResponse:
    service = AplicacionService(db)
    return service.obtener_aplicacion(aplicacion_id)

@router.delete("/{aplicacion_id}", status_code=204)
def eliminar_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
) -> None:
    service = AplicacionService(db)
    service.eliminar_aplicacion(aplicacion_id)

@router.patch("/{aplicacion_id}/estatus", response_model=AplicacionResponse)
def cambiar_estatus(
    aplicacion_id: int,
    datos: CambioEstatusRequest,
    db: Session = Depends(get_db),
) -> AplicacionResponse:
    service = AplicacionService(db)
    return service.cambiar_estatus(
    aplicacion_id,
    datos.nuevo_estatus,
    )