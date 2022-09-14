"""
Cit Dias Inhabiles v2, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitDiaInhabilOut(BaseModel):
    """Esquema para entregar dias inhabiles"""

    id: int
    fecha: date
    descripcion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitDiaInhabilOut(CitDiaInhabilOut, OneBaseOut):
    """Esquema para entregar un dia inhabil"""
