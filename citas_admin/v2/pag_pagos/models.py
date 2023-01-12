"""
Pagos Pagos v2, modelos
"""
from collections import OrderedDict
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class PagPago(Base, UniversalMixin):
    """PagPago"""

    ESTADOS = OrderedDict(
        [
            ("SOLICITADO", "Solicitado"),  # Cuando se crea el pago en espera de que el banco lo procese
            ("CANCELADO", "Cancelado"),  # Cuando pasa mucho tiempo y no hay respuesta del banco, se cancela
            ("PAGADO", "Pagado"),  # Cuando el banco procesa el pago con exito
            ("FALLIDO", "Fallido"),  # Cuando el banco reporta que falla el pago
        ]
    )

    # Nombre de la tabla
    __tablename__ = "pag_pagos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="pag_pagos")
    pag_tramite_servicio_id = Column(Integer, ForeignKey("pag_tramites_servicios.id"), index=True, nullable=False)
    pag_tramite_servicio = relationship("PagTramiteServicio", back_populates="pag_pagos")

    # Columnas
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False), nullable=False)
    email = Column(String(256), nullable=False, default="")  # Email opcional si el cliente desea que se le envie el comprobante a otra dirección
    folio = Column(String(256), nullable=False, default="")
    total = Column(Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=False)
    ya_se_envio_comprobante = Column(Boolean, nullable=False, default=False)

    @property
    def cit_cliente_nombre(self):
        """Nombre del cliente"""
        return self.cit_cliente.nombre

    @property
    def cit_cliente_curp(self):
        """Curp del cliente"""
        return self.cit_cliente.curp

    @property
    def cit_cliente_email(self):
        """Email del cliente"""
        return self.cit_cliente.email

    @property
    def pag_tramite_servicio_clave(self):
        """Clave del tramite o servicio"""
        return self.pag_tramite_servicio.clave

    @property
    def pag_tramite_servicio_descripcion(self):
        """Descripcion del tramite o servicio"""
        return self.pag_tramite_servicio.descripcion

    def __repr__(self):
        """Representación"""
        return f"<PagPago {self.id}>"
