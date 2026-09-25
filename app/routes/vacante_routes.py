from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.vacante import VacanteCreate, VacanteResponse, VacanteUpdate
from app.services.vacante_service import VacanteService

router = APIRouter(prefix="/vacantes", tags=["Vacantes"])

@router.post("/", response_model=VacanteResponse, status_code=201)
def crear_vacante(datos: VacanteCreate, db: Session = Depends(get_db)) -> VacanteResponse:
    """Registra una nueva vacante."""
    service = VacanteService(db)
    return service.crear_vacante(**datos.model_dump())


@router.get("/empresa/{empresa_id}", response_model=list[VacanteResponse])
def listar_vacantes(empresa_id: int, db: Session = Depends(get_db)) -> list[VacanteResponse]:
    """Lista todas las vacantes por empresas registradas."""
    service = VacanteService(db)    
    return service.listar_vacantes_de_empresa(empresa_id)

@router.get("/{vacante_id}", response_model=VacanteResponse)
def obtener_vacante(vacante_id: int, db: Session = Depends(get_db)) -> VacanteResponse:
    """Obtiene una vacante por su id."""
    service = VacanteService(db)
    return service.obtener_vacante(vacante_id)

@router.patch("/{vacante_id}", response_model=VacanteResponse)
def actualizar_vacante(vacante_id: int, datos: VacanteUpdate, db: Session = Depends(get_db)) -> VacanteResponse:
    """Actualiza parcialmente una vacante existente."""
    service = VacanteService(db)
    datos_a_actualizar = datos.model_dump(exclude_unset=True)
    return service.actualizar_vacante(vacante_id, datos_a_actualizar)


@router.delete("/{vacante_id}", status_code=204)
def eliminar_vacante(vacante_id: int, db: Session = Depends(get_db)) -> None:
    """Elimina una vacante existente."""
    service = VacanteService(db)
    service.eliminar_vacante(vacante_id)
        