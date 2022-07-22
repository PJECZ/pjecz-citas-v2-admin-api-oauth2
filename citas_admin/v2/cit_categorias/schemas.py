"""
Cit Categorias v2, esquemas de pydantic
"""
from pydantic import BaseModel


class CitCategoriaOut(BaseModel):
    """Esquema para entregar categorias"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
