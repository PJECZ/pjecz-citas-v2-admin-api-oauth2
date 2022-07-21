"""
Materias v2, esquemas de pydantic
"""
from pydantic import BaseModel


class MateriaOut(BaseModel):
    """Esquema para entregar materias"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
