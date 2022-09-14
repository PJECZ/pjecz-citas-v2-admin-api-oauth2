"""
Cit Clientes Recuperaciones v2, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones de clientes"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    expiracion: datetime
    cadena_validar: str
    mensajes_cantidad: int
    ya_recuperado: bool
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitClienteRecuperacionOut(CitClienteRecuperacionOut, OneBaseOut):
    """Esquema para entregar una recuperacion"""


class CitClientesRecuperacionesCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de recuperaciones creadas por dia"""

    items: dict
    total: int
