"""Endpoints CRUD para la entidad Empresa."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from app.services.empresa_service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["Empresas"])


@router.post("/", response_model=EmpresaResponse, status_code=201)
def crear_empresa(datos: EmpresaCreate, db: Session = Depends(get_db)) -> EmpresaResponse:
    """Registra una nueva empresa."""
    service = EmpresaService(db)
    return service.crear_empresa(**datos.model_dump())


@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)) -> list[EmpresaResponse]:
    """Lista todas las empresas registradas."""
    service = EmpresaService(db)    
    return service.listar_empresas()


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)) -> EmpresaResponse:
    """Obtiene una empresa por su id."""
    service = EmpresaService(db)
    return service.obtener_empresa(empresa_id)  

@router.patch("/{empresa_id}", response_model=EmpresaResponse)
def actualizar_empresa(empresa_id: int, datos: EmpresaUpdate, db: Session = Depends(get_db)) -> EmpresaResponse:
    """Actualiza parcialmente una empresa existente."""
    service = EmpresaService(db)
    datos_a_actualizar = datos.model_dump(exclude_unset=True)
    return service.actualizar_empresa(empresa_id, datos_a_actualizar)


@router.delete("/{empresa_id}", status_code=204)
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db)) -> None:
    """Elimina una empresa existente."""
    service = EmpresaService(db)
    service.eliminar_empresa(empresa_id)