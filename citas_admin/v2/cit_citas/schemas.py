"""
Cit Citas v2, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int | None
    cit_cliente_id: int | None
    cit_cliente_nombre: str | None
    cit_cliente_curp: str | None
    cit_cliente_email: str | None
    cit_servicio_id: int | None
    cit_servicio_clave: str | None
    cit_servicio_descripcion: str | None
    oficina_id: int | None
    oficina_clave: str | None
    oficina_descripcion: str | None
    oficina_descripcion_corta: str | None
    inicio: datetime | None
    termino: datetime | None
    notas: str | None
    estado: str | None
    asistencia: bool | None
    codigo_asistencia: str | None
    creado: datetime | None

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
