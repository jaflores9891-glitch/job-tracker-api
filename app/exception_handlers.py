"""Manejadores globales de excepciones de dominio."""
from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.exceptions import (
    AplicacionNoEncontradaError,
    DominioError,
    EmpresaDuplicadaError,
    EmpresaNoEncontradaError,
    TransicionInvalidaError,
    VacanteNoEncontradaError,
)


async def manejar_no_encontrado(request: Request, exc: DominioError) -> JSONResponse:
    """Traduce errores de 'no encontrado' a HTTP 404."""
    return JSONResponse(status_code=404, content={"detalle": str(exc)})

async def manejar_conflicto(request: Request, exc: DominioError) -> JSONResponse:
    """Traduce errores de duplicados/transiciones inválidas a HTTP 409."""
    return JSONResponse(status_code=409, content={"detalle": str(exc)})

def registrar_manejadores(app) -> None:
    """Registra todos los manejadores de excepciones en la app de FastAPI."""
    app.add_exception_handler(EmpresaNoEncontradaError, manejar_no_encontrado)
    app.add_exception_handler(VacanteNoEncontradaError, manejar_no_encontrado)
    app.add_exception_handler(AplicacionNoEncontradaError, manejar_no_encontrado)
    app.add_exception_handler(EmpresaDuplicadaError, manejar_conflicto)
    app.add_exception_handler(TransicionInvalidaError, manejar_conflicto)
    