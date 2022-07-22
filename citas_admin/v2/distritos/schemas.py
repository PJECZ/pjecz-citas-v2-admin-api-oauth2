"""
Distritos v2, esquemas de pydantic
"""
from pydantic import BaseModel


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id: int
    nombre: str
    nombre_corto: str
    es_distrito_judicial: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
