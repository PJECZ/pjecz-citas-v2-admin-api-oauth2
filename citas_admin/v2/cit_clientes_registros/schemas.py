"""
Cit Clientes Registros v2, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitClienteRegistroOut(BaseModel):
    """Esquema para entregar registros de clientes"""

    id: int
    nombres: str
    apellido_primero: str
    apellido_segundo: str
    curp: str
    telefono: str
    email: str
    expiracion: datetime
    cadena_validar: str
    mensajes_cantidad: int
    ya_registrado: bool
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitClienteRegistroOut(CitClienteRegistroOut, OneBaseOut):
    """Esquema para entregar un registro de cliente"""


class CitClientesRegistrosCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de registros creados por dia"""

    items: dict
    total: int
