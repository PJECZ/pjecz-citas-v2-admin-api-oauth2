"""
Cit Citas v2, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    cit_servicio_id: int
    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime
    notas: str
    estado: str
    asistencia: bool
    codigo_asistencia: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitCitaOut(CitCitaOut, OneBaseOut):
    """Esquema para entregar una cita"""


class CitCitasCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de citas creadas por dia"""

    items: dict
    total: int


class CitCitasAgendadasPorServicioOficinaOut(BaseModel):
    """Esquema para entregar cantidades de citas agendadas por servicio y oficina"""

    items: list
    total: int
