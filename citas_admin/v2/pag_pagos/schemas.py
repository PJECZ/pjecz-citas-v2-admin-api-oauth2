"""
Pagos Pagos v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PagPagoOut(BaseModel):
    """Esquema para entregar pagos"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    pag_tramite_servicio_id: int
    pag_tramite_servicio_clave: str
    pag_tramite_servicio_descripcion: str
    total: float
    estado: str
    email: str
    ya_se_envio_comprobante: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePagPagoOut(PagPagoOut, OneBaseOut):
    """Esquema para entregar un servicio"""
