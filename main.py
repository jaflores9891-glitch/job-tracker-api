"""Punto de entrada de la aplicación FastAPI."""
from fastapi import FastAPI

from app.logging_config import configurar_logging
from app.routes.empresa_routes import router as empresa_router
from app.routes.vacante_routes import router as vacante_router
from app.routes.aplicacion_routes import router as aplicacion_router

from app.exception_handlers import registrar_manejadores

configurar_logging()

app = FastAPI(
    title="Job Application Tracker API",
    description="API para registrar empresas, vacantes y aplicaciones de trabajo.",
    version="0.1.0",
)

registrar_manejadores(app)      # <- esta línea faltaba

app.include_router(empresa_router)
app.include_router(vacante_router)
app.include_router(aplicacion_router)

@app.get("/")
def raiz() -> dict[str, str]:
    """Endpoint de verificación rápida de que la API está viva."""
    return {"mensaje": "Job Tracker API funcionando correctamente."}

