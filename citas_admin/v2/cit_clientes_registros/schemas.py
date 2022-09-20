"""
Cit Clientes Registros v2, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitClienteRegistroOut(BaseModel):
    """Esquema para entregar registros de clientes"""

    id: int | None
    nombres: str | None
    apellido_primero: str | None
    apellido_segundo: str | None
    curp: str | None
    telefono: str | None
    email: str | None
    expiracion: datetime | None
    cadena_validar: str | None
    mensajes_cantidad: int | None
    ya_registrado: bool | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitClienteRegistroOut(CitClienteRegistroOut, OneBaseOut):
    """Esquema para entregar un registro de cliente"""


class CitClientesRegistrosCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de registros creados por dia"""

    creado: date
    cantidad: int
