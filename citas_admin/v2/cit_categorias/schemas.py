"""
Cit Categorias v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitCategoriaOut(BaseModel):
    """Esquema para entregar categorias"""

    id: int | None
    nombre: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitCategoriaOut(CitCategoriaOut, OneBaseOut):
    """Esquema para entregar una categoria"""
