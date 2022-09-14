"""
Cit Servicios v2, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitServicioOut(BaseModel):
    """Esquema para entregar servicios"""

    id: int | None
    cit_categoria_id: int | None
    cit_categoria_nombre: str | None
    clave: str | None
    descripcion: str | None
    duracion: time | None
    documentos_limite: int | None
    desde: time | None
    hasta: time | None
    dias_habilitados: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitServicioOut(CitServicioOut, OneBaseOut):
    """Esquema para entregar un servicio"""
