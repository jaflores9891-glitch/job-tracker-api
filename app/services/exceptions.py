"""Excepciones propias del dominio de negocio."""


class DominioError(Exception):
    """Excepción base de la que heredan todos los errores de negocio."""


class EmpresaNoEncontradaError(DominioError):
    """Se lanza cuando no existe una empresa con el ID solicitado."""

    def __init__(self, empresa_id: int) -> None:
        """Inicializa el error con el ID de la empresa no encontrada."""
        self.empresa_id = empresa_id
        super().__init__(f"No existe una empresa con id={empresa_id}")


class VacanteNoEncontradaError(DominioError):
    """Se lanza cuando no existe una vacante con el ID solicitado."""

    def __init__(self, vacante_id: int) -> None:
        """Inicializa el error con el ID de la vacante no encontrada."""
        self.vacante_id = vacante_id
        super().__init__(f"No existe una vacante con id={vacante_id}")


class AplicacionNoEncontradaError(DominioError):
    """Se lanza cuando no existe una aplicación con el ID solicitado."""

    def __init__(self, aplicacion_id: int) -> None:
        """Inicializa el error con el ID de la aplicación no encontrada."""
        self.aplicacion_id = aplicacion_id
        super().__init__(f"No existe una aplicación con id={aplicacion_id}")


class EmpresaDuplicadaError(DominioError):
    """Se lanza al intentar crear una empresa con un nombre ya existente."""

    def __init__(self, nombre: str) -> None:
        """Inicializa el error con el nombre de empresa duplicado."""
        self.nombre = nombre
        super().__init__(f"Ya existe una empresa con el nombre '{nombre}'")


class TransicionInvalidaError(DominioError):
    """Se lanza al intentar un cambio de estatus no permitido."""

    def __init__(self, estatus_actual: str, estatus_nuevo: str) -> None:
        """Inicializa el error con el estatus actual y el estatus destino."""
        self.estatus_actual = estatus_actual
        self.estatus_nuevo = estatus_nuevo
        super().__init__(
            f"No se puede pasar de '{estatus_actual}' a '{estatus_nuevo}'"
        )