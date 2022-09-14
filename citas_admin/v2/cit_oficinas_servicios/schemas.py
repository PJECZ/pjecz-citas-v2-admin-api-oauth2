"""
Cit Oficinas-Servicios v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitOficinaServicioOut(BaseModel):
    """Esquema para entregar oficinas-servicios"""

    id: int | None
    cit_servicio_id: int | None
    cit_servicio_clave: str | None
    cit_servicio_descripcion: str | None
    oficina_id: int | None
    oficina_clave: str | None
    oficina_descripcion: str | None
    oficina_descripcion_corta: str | None
    descripcion: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitOficinaServicioOut(CitOficinaServicioOut, OneBaseOut):
    """Esquema para entregar una oficina-servicio"""
