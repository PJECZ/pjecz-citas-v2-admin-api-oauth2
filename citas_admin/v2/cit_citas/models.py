"""
Cit Citas v2, modelos
"""
from collections import OrderedDict
from datetime import datetime

import pytz
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitCita(Base, UniversalMixin):
    """CitCita"""

    ESTADOS = OrderedDict(
        [
            ("ASISTIO", "Asistió"),
            ("CANCELO", "Canceló"),
            ("INASISTENCIA", "Inasistencia"),
            ("PENDIENTE", "Pendiente"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "cit_citas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="cit_citas")
    cit_servicio_id = Column(Integer, ForeignKey("cit_servicios.id"), index=True, nullable=False)
    cit_servicio = relationship("CitServicio", back_populates="cit_citas")
    oficina_id = Column(Integer, ForeignKey("oficinas.id"), index=True, nullable=False)
    oficina = relationship("Oficina", back_populates="cit_citas")

    # Columnas
    inicio = Column(DateTime(), nullable=False)
    termino = Column(DateTime(), nullable=False)
    notas = Column(Text(), nullable=False)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False))
    asistencia = Column(Boolean, nullable=False, default=False)
    codigo_asistencia = Column(String(4))
    cancelar_antes = Column(DateTime())

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
    def cit_servicio_clave(self):
        """Clave del servicio"""
        return self.cit_servicio.clave

    @property
    def cit_servicio_descripcion(self):
        """Descripción del servicio"""
        return self.cit_servicio.descripcion

    @property
    def puede_cancelarse(self):
        """Puede cancelarse esta cita?"""
        if self.estado != "PENDIENTE":
            return False
        if self.cancelar_antes is None:
            return True
        america_mexico_city_dt = datetime.now(tz=pytz.timezone("America/Mexico_City"))
        now_without_tz = america_mexico_city_dt.replace(tzinfo=None)
        return now_without_tz < self.cancelar_antes

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
        return f"<CitCita {self.id}>"
