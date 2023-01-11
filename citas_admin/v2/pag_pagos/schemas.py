"""
Pagos Pagos v2, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PagPagoOut(BaseModel):
    """Esquema para entregar pagos"""

    id: int | None
    cit_cliente_id: int | None
    cit_cliente_nombre: str | None
    cit_cliente_curp: str | None
    cit_cliente_email: str | None
    pag_tramite_servicio_id: int | None
    pag_tramite_servicio_clave: str | None
    pag_tramite_servicio_descripcion: str | None
    total: float | None
    estado: str | None
    email: str | None
    ya_se_envio_comprobante: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePagPagoOut(PagPagoOut, OneBaseOut):
    """Esquema para entregar un pago"""
