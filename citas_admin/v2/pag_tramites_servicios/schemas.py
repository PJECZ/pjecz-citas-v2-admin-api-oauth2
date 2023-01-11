"""
Pagos Tramites y Servicios v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PagTramiteServicioOut(BaseModel):
    """Esquema para entregar tramites y servicios"""

    id: int
    clave: str
    descripcion: str
    costo: float
    url: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePagTramiteServicioOut(PagTramiteServicioOut, OneBaseOut):
    """Esquema para entregar un servicio"""
