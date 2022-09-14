"""
Encuestas Servicios v2, esquemas de pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class EncServicioOut(BaseModel):
    """Esquema para entregar encuesta de servicio"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    respuesta_01: Optional[int] = None
    respuesta_02: Optional[int] = None
    respuesta_03: Optional[int] = None
    respuesta_03: Optional[str] = ""
    estado: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneEncServicioOut(EncServicioOut, OneBaseOut):
    """Esquema para entregar una encuesta de servicio"""
