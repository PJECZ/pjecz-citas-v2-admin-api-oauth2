"""
Cit Clientes Recuperaciones v2, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones de clientes"""

    id: int | None
    cit_cliente_id: int | None
    cit_cliente_nombre: str | None
    cit_cliente_curp: str | None
    cit_cliente_email: str | None
    expiracion: datetime | None
    cadena_validar: str | None
    mensajes_cantidad: int | None
    ya_recuperado: bool | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitClienteRecuperacionOut(CitClienteRecuperacionOut, OneBaseOut):
    """Esquema para entregar una recuperacion"""


class CitClientesRecuperacionesCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de recuperaciones creadas por dia"""

    items: dict
    total: int
