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
    total = Column(Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=False)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False), nullable=False)
    email = Column(String(256))  # Email opcional si el cliente desea que se le envie el comprobante a otra dirección
    ya_se_envio_comprobante = Column(Boolean, default=False)

    def __repr__(self):
        """Representación"""
        return f"<PagPago {self.id}>"
