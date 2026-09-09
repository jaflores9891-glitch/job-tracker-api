"""Configuración centralizada de logging para el proyecto."""
import logging


def configurar_logging() -> None:
    """Configura el formato y nivel de logging para toda la aplicación."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )