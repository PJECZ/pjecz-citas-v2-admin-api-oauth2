"""
Roles v2, esquemas de pydantic
"""
from pydantic import BaseModel


class RolOut(BaseModel):
    """Esquema para entregar roles"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
