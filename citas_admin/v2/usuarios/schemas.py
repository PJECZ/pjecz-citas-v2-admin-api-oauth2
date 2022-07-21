"""
Usuarios v2, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class UsuarioOut(BaseModel):
    """Esquema para entregar usuarios"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_id: int
    autoridad_clave: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    domicilio_completo: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
