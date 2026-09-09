"""Modelo de la entidad Vacante."""
from datetime import date

from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Vacante(Base):

    __tablename__ = "vacantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    salario_estimado: Mapped[int] = mapped_column(Integer, nullable=True)
    modalidad: Mapped[str] = mapped_column(String(20), nullable=True)
    tecnologias: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    fecha_publicacion: Mapped[date] = mapped_column(Date, nullable=True)

    empresa: Mapped["Empresa"] = relationship(back_populates="vacantes")

    def __repr__(self) -> str:
        return f"<Vacante id={self.id} titulo={self.titulo!r}>"