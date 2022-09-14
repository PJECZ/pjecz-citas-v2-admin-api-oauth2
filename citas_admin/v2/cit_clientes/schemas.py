"""
Cit Clientes v2, esquemas de pydantic
"""
from typing import Dict, Optional
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    id: int
    nombres: str
    apellido_primero: str
    apellido_segundo: str
    nombre: str
    curp: str
    telefono: str
    email: str
    contrasena_md5: str
    contrasena_sha256: str
    renovacion: date
    limite_citas_pendientes: Optional[int]
    enviar_boletin: bool
    es_adulto_mayor: bool
    es_mujer: bool
    es_identidad: bool
    es_discapacidad: bool
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitClienteOut(CitClienteOut, OneBaseOut):
    """Esquema para entregar un cliente"""


class CitClienteCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de clientes creados por dia"""

    items: dict
    total: int
