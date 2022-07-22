"""
Cit Clientes v2, modelos
"""
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitCliente(Base, UniversalMixin):
    """CitCliente"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombres = Column(String(256), nullable=False)
    apellido_primero = Column(String(256), nullable=False)
    apellido_segundo = Column(String(256), nullable=False)
    curp = Column(String(18), unique=True, nullable=False)
    telefono = Column(String(64), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    contrasena_md5 = Column(String(256), nullable=False)
    contrasena_sha256 = Column(String(256), nullable=False)
    renovacion = Column(Date(), nullable=False)

    # Hijos
    cit_citas = relationship("CitCita", back_populates="cit_cliente")
    cit_clientes_recuperaciones = relationship("CitClienteRecuperacion", back_populates="cit_cliente")

    @property
    def nombre(self):
        """Junta nombres, apellido_primero y apellido segundo"""
        return self.nombres + " " + self.apellido_primero + " " + self.apellido_segundo

    def __repr__(self):
        """Representación"""
        return f"<CitCliente {self.email}>"
