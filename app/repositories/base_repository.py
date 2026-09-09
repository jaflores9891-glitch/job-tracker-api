"""Repositorio base genérico con operaciones CRUD comunes."""
from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.orm import Session

from app.database import Base

T = TypeVar("T", bound=Base)

class RepositorioBase(Generic[T]):

    def __init__(self, db: Session, modelo: Type[T]) -> None:
        self.db = db
        self.modelo = modelo

    def crear(self, objeto: T) -> T:
        self.db.add(objeto)
        self.db.commit()
        self.db.refresh(objeto)
        return objeto

    def obtener_por_id(self, id: int) -> Optional[T]:
        return self.db.query(self.modelo).filter(self.modelo.id == id).first()

    def obtener_todos(self) -> list[T]:
        return self.db.query(self.modelo).all()

    def actualizar(self, objeto: T) -> T:
        self.db.commit()
        self.db.refresh(objeto)
        return objeto

    def eliminar(self, id: int) -> bool:
        objeto = self.obtener_por_id(id)
        if objeto is None:
            return False
        self.db.delete(objeto)
        self.db.commit()
        return True