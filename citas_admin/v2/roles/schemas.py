"""
Roles v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class RolOut(BaseModel):
    """Esquema para entregar roles"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneRolOut(RolOut, OneBaseOut):
    """Esquema para entregar un rol"""
