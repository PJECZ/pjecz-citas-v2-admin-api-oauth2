"""
Encuestas Sistemas v2, esquemas de pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EncSistemaOut(BaseModel):
    """Esquema para entregar encuestas de sistemas"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_email: str
    respuesta_01: Optional[int] = None
    respuesta_02: Optional[str] = ""
    respuesta_03: Optional[str] = ""
    estado: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
