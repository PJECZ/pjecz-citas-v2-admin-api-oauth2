"""
Pagos Tramites y Servicios v2, esquemas de pydantic
"""
from pydantic import BaseModel


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
