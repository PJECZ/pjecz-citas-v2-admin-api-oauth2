"""
Pagos Tramites y Servicios v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PagTramiteServicioOut(BaseModel):
    """Esquema para entregar tramites y servicios"""

    id: int | None
    clave: str | None
    descripcion: str | None
    costo: float | None
    url: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePagTramiteServicioOut(PagTramiteServicioOut, OneBaseOut):
    """Esquema para entregar un tramite y servicio"""
