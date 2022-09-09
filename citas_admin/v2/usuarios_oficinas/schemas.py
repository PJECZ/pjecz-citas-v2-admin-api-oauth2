"""
Usuarios-Oficinas v2, esquemas de pydantic
"""
from pydantic import BaseModel


class UsuarioOficinaOut(BaseModel):
    """Esquema para entregar usuario-oficina"""

    id: int
    oficina_id: int
    oficina_nombre: str
    usuario_id: int
    usuario_nombre: str
    descripcion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
