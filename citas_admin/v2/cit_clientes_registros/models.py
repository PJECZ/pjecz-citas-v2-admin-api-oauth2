"""
Cit Clientes Registros v2, modelos
"""
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitClienteRegistro(Base, UniversalMixin):
    """CitClienteRegistro"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes_registros"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombres = Column(String(256), nullable=False)
    apellido_primero = Column(String(256), nullable=False)
    apellido_segundo = Column(String(256), nullable=False)
    curp = Column(String(18), nullable=False, index=True)
    telefono = Column(String(64), nullable=False)
    email = Column(String(256), nullable=False, index=True)
    expiracion = Column(DateTime(), nullable=False)
    cadena_validar = Column(String(256), nullable=False)
    mensajes_cantidad = Column(Integer(), nullable=False, default=0)
    ya_registrado = Column(Boolean(), nullable=False, default=False)

    def __repr__(self):
        """Representación"""
        return f"<CitClienteRegistro {self.id}>"
