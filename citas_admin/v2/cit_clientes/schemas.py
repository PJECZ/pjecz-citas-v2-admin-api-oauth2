"""
Cit Clientes v2, esquemas de pydantic
"""
from typing import Dict, Optional
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    id: int | None
    nombres: str | None
    apellido_primero: str | None
    apellido_segundo: str | None
    nombre: str | None
    curp: str | None
    telefono: str | None
    email: str | None
    contrasena_md5: str | None
    contrasena_sha256: str | None
    renovacion: date | None
    limite_citas_pendientes: Optional[int] | None
    enviar_boletin: bool | None
    es_adulto_mayor: bool | None
    es_mujer: bool | None
    es_identidad: bool | None
    es_discapacidad: bool | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitClienteOut(CitClienteOut, OneBaseOut):
    """Esquema para entregar un cliente"""


class CitClienteCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de clientes creados por dia"""

    items: dict
    total: int
