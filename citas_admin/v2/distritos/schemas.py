"""
Distritos v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id: int | None
    nombre: str | None
    nombre_corto: str | None
    es_distrito_judicial: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
