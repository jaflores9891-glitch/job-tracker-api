"""Punto de entrada de la aplicación FastAPI."""
from fastapi import FastAPI

from app.logging_config import configurar_logging

configurar_logging()

app = FastAPI(
    title="Job Application Tracker API",
    description="API para registrar empresas, vacantes y aplicaciones de trabajo.",
    version="0.1.0",
)


@app.get("/")
def raiz() -> dict[str, str]:
    """Endpoint de verificación rápida de que la API está viva."""
    return {"mensaje": "Job Tracker API funcionando correctamente."}