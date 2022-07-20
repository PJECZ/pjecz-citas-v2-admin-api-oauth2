"""
Cit Dias Inhabiles v2, modelos
"""
from sqlalchemy import Column, Date, Integer, String

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitDiaInhabil(Base, UniversalMixin):
    """CitDiaInhabil"""

    # Nombre de la tabla
    __tablename__ = "cit_dias_inhabiles"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    fecha = Column(Date(), unique=True, nullable=False)
    descripcion = Column(String(256), nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<CitDiaInhabil {self.fecha}>"
