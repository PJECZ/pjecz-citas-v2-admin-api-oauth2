"""
Encuestas Sistemas v2, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class EncSistemaOut(BaseModel):
    """Esquema para entregar encuestas de sistemas"""

    id: int | None
    cit_cliente_id: int | None
    cit_cliente_nombre: str | None
    cit_cliente_email: str | None
    respuesta_01: int | None
    respuesta_02: str | None
    respuesta_03: str | None
    estado: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneEncSistemaOut(EncSistemaOut, OneBaseOut):
    """Esquema para entregar una encuesta de sistema"""
