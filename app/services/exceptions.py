"""Excepciones propias del dominio de negocio."""


class DominioError(Exception):
    """Excepción base de la que heredan todos los errores de negocio."""
    pass


class EmpresaNoEncontradaError(DominioError):

    def __init__(self, empresa_id: int) -> None:
        self.empresa_id = empresa_id
        super().__init__(f"No existe una empresa con id={empresa_id}")


class VacanteNoEncontradaError(DominioError):

    def __init__(self, vacante_id: int) -> None:
        self.vacante_id = vacante_id
        super().__init__(f"No existe una vacante con id={vacante_id}")


class AplicacionNoEncontradaError(DominioError):

    def __init__(self, aplicacion_id: int) -> None:
        self.aplicacion_id = aplicacion_id
        super().__init__(f"No existe una aplicación con id={aplicacion_id}")


class EmpresaDuplicadaError(DominioError):

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        super().__init__(f"Ya existe una empresa con el nombre '{nombre}'")

class TransicionInvalidaError(DominioError):
    """Se lanza al intentar un cambio de estatus no permitido."""

    def __init__(self, estatus_actual: str, estatus_nuevo: str) -> None:

        self.estatus_actual = estatus_actual
        self.estatus_nuevo = estatus_nuevo
        super().__init__(
            f"No se puede pasar de '{estatus_actual}' a '{estatus_nuevo}'"
        )