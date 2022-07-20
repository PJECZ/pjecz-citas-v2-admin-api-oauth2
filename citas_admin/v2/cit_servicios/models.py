"""
Cit Servicios v2, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitServicio(Base, UniversalMixin):
    """CitServicio"""

    # Nombre de la tabla
    __tablename__ = "cit_servicios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    cit_categoria_id = Column(Integer, ForeignKey("cit_categorias.id"), index=True, nullable=False)
    cit_categoria = relationship("CitCategoria", back_populates="cit_servicios")

    # Columnas
    clave = Column(String(32), unique=True, nullable=False)
    descripcion = Column(String(64), nullable=False)
    duracion = Column(Time(), nullable=False)
    documentos_limite = Column(Integer, nullable=False)

    # Hijos
    cit_citas = relationship("CitCita", back_populates="cit_servicio")
    cit_oficinas_servicios = relationship("CitOficinaServicio", back_populates="cit_servicio")

    def __repr__(self):
        """Representación"""
        return f"<CitServicio {self.id}>"
