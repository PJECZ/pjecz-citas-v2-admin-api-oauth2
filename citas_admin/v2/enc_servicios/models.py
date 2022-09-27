"""
Encuestas Servicios v2, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class EncServicio(Base, UniversalMixin):
    """EncServicio"""

    ESTADOS = OrderedDict(
        [
            ("PENDIENTE", "Pendiente"),
            ("CANCELADO", "Cancelado"),
            ("CONTESTADO", "Contestado"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "enc_servicios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="enc_servicios")
    oficina_id = Column(Integer, ForeignKey("oficinas.id"), nullable=False)
    oficina = relationship("Oficina", back_populates="enc_servicios")

    # Columnas
    respuesta_01 = Column(Integer(), nullable=True)
    respuesta_02 = Column(Integer(), nullable=True)
    respuesta_03 = Column(Integer(), nullable=True)
    respuesta_04 = Column(String(512), nullable=True)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False))

    @property
    def cit_cliente_email(self):
        """Retorna el email del cliente"""
        return self.cit_cliente.email

    @property
    def cit_cliente_nombre(self):
        """Retorna el nombre del cliente"""
        return self.cit_cliente.nombre

    @property
    def oficina_clave(self):
        """Clave de la oficina"""
        return self.oficina.clave

    @property
    def oficina_descripcion(self):
        """Descripcion de la oficina"""
        return self.oficina.descripcion

    @property
    def oficina_descripcion_corta(self):
        """Descripcion corta de la oficina"""
        return self.oficina.descripcion_corta

    def __repr__(self):
        """Representación"""
        return f"<EncServicio {self.id}>"
