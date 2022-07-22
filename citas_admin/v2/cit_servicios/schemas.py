"""
Cit Servicios v2, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel


class CitServicioOut(BaseModel):
    """Esquema para entregar servicios"""

    id: int
    cit_categoria_id: int
    cit_categoria_nombre: str
    clave: str
    descripcion: str
    duracion: time
    documentos_limite: int

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
