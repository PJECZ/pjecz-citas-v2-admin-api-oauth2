"""
Pagos Pagos v2, esquemas de pydantic
"""
from pydantic import BaseModel


class PagPagoOut(BaseModel):
    """Esquema para entregar pagos"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    total: float
    estado: str
    email: str
    ya_se_envio_comprobante: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
