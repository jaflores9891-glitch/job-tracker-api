"""Repositorio base genérico con operaciones CRUD comunes."""
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.database import Base

T = TypeVar("T", bound=Base)


class RepositorioBase(Generic[T]):
    """Operaciones CRUD genéricas reutilizables por cualquier entidad.

    Las clases concretas (por ejemplo, "RepositorioEmpresa") heredan de
    esta clase indicando su modelo de SQLAlchemy como parámetro genérico.
    """

    def __init__(self, db: Session, modelo: Type[T]) -> None:
        """Inicializa el repositorio con una sesión y su tipo de modelo."""
        self.db = db
        self.modelo = modelo

    def crear(self, objeto: T) -> T:
        """Guarda un nuevo objeto en la base de datos y lo devuelve actualizado desde la base de datos."""
        self.db.add(objeto)
        self.db.commit()
        self.db.refresh(objeto)
        return objeto

    def obtener_por_id(self, id: int) -> Optional[T]:
        """Devuelve el objeto con el ID indicado, o `None` si no existe."""
        return self.db.query(self.modelo).filter(self.modelo.id == id).first()

    def obtener_todos(self) -> list[T]:
        """Devuelve todos los objetos del modelo de este repositorio."""
        return self.db.query(self.modelo).all()

    def actualizar(self, objeto: T) -> T:
        """Confirma los cambios pendientes de un objeto y lo devuelve actualizado."""
        self.db.commit()
        self.db.refresh(objeto)
        return objeto

    def eliminar(self, id: int) -> bool:
        """Elimina el objeto con el ID indicado.

        Returns:
            Verdadero si el objeto existía y fue eliminado; falso en caso contrario.
        """
        objeto = self.obtener_por_id(id)
        if objeto is None:
            return False
        self.db.delete(objeto)
        self.db.commit()
        return True