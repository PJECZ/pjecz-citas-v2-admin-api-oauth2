"""
Usuarios-Oficinas v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class UsuarioOficinaOut(BaseModel):
    """Esquema para entregar usuario-oficina"""

    id: int | None
    oficina_id: int | None
    oficina_nombre: str | None
    usuario_id: int | None
    usuario_nombre: str | None
    descripcion: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneUsuarioOficinaOut(UsuarioOficinaOut, OneBaseOut):
    """Esquema para entregar un usuario-oficina"""
