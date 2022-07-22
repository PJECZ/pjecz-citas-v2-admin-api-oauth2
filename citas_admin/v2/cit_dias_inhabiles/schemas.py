"""
Cit Dias Inhabiles v2, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


class CitDiaInhabilOut(BaseModel):
    """Esquema para entregar dias inhabiles"""

    id: int
    fecha: date
    descripcion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
