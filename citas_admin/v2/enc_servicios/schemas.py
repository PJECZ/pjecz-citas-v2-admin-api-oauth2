"""
Encuestas Servicios v2, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class EncServicioOut(BaseModel):
    """Esquema para entregar encuesta de servicio"""

    id: int | None
    cit_cliente_id: int | None
    cit_cliente_nombre: str | None
    cit_cliente_curp: str | None
    cit_cliente_email: str | None
    oficina_id: int | None
    oficina_clave: str | None
    oficina_descripcion: str | None
    oficina_descripcion_corta: str | None
    respuesta_01: int | None
    respuesta_02: int | None
    respuesta_03: int | None
    respuesta_03: str | None
    estado: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneEncServicioOut(EncServicioOut, OneBaseOut):
    """Esquema para entregar una encuesta de servicio"""
