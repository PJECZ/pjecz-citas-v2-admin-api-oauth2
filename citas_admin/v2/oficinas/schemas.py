"""
Oficinas v2, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    domicilio_id: int
    domicilio_completo: str
    apertura: time
    cierre: time
    clave: str
    descripcion: str
    descripcion_corta: str
    es_jurisdiccional: bool
    limite_personas: int
    puede_agendar_citas: bool
    puede_enviar_qr: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneOficinaOut(OficinaOut, OneBaseOut):
    """Esquema para entregar una oficina"""
