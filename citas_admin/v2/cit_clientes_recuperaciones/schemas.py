"""
Cit Clientes Recuperaciones v2, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones de clientes"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    expiracion: datetime
    cadena_validar: str
    mensajes_cantidad: int
    ya_recuperado: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
