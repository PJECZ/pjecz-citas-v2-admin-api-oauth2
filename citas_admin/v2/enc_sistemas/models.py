"""
Encuestas Sistemas v2, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class EncSistema(Base, UniversalMixin):
    """EncSistema"""

    ESTADOS = OrderedDict(
        [
            ("PENDIENTE", "Pendiente"),
            ("CANCELADO", "Cancelado"),
            ("CONTESTADO", "Contestado"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "enc_sistemas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="enc_sistemas")

    # Columnas
    respuesta_01 = Column(Integer(), nullable=True)
    respuesta_02 = Column(String(255), nullable=True)
    respuesta_03 = Column(String(255), nullable=True)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False))

    @property
    def cit_cliente_email(self):
        """Retorna el email del cliente"""
        return self.cit_cliente.email

    @property
    def cit_cliente_nombre(self):
        """Retorna el nombre del cliente"""
        return self.cit_cliente.nombre

    def __repr__(self):
        """Representación"""
        return f"<EncSistema {self.id}>"
