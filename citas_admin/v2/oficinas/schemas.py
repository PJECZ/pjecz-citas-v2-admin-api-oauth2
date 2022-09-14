"""
Oficinas v2, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    domicilio_id: int | None
    domicilio_completo: str | None
    apertura: time | None
    cierre: time | None
    clave: str | None
    descripcion: str | None
    descripcion_corta: str | None
    es_jurisdiccional: bool | None
    limite_personas: int | None
    puede_agendar_citas: bool | None
    puede_enviar_qr: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneOficinaOut(OficinaOut, OneBaseOut):
    """Esquema para entregar una oficina"""
