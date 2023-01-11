"""
Pagos Pagos v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave, safe_curp, safe_email, safe_string

from .models import PagPago
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente


def get_pag_pagos(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    pag_tramite_servicio_id: int = None,
    estado: str = None,
    estatus: str = None,
    ya_se_envio_comprobante: bool = None,
) -> Any:
    """Consultar los pagos activos"""

    # Consulta
    consulta = db.query(PagPago)

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(PagPago.cit_cliente == cit_cliente)
    elif cit_cliente_curp is not None:
        cit_cliente_curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if cit_cliente_curp is None or cit_cliente_curp == "":
            raise CitasNotValidParamError("No es válido el CURP")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.curp == cit_cliente_curp)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=False)
        if cit_cliente_email is None or cit_cliente_email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por tramite y servicio
    if pag_tramite_servicio_id is not None:
        consulta = consulta.filter_by(pag_tramite_servicio_id=pag_tramite_servicio_id)

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado in PagPago.ESTADOS:
            consulta = consulta.filter_by(estado=estado)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por ya_se_envio_comprobante
    if ya_se_envio_comprobante is not None:
        consulta = consulta.filter_by(ya_se_envio_comprobante=ya_se_envio_comprobante)

    # Entregar
    return consulta.order_by(PagPago.id)


def get_pag_pago(db: Session, pag_pago_id: int) -> PagPago:
    """Consultar un pago por su id"""
    pag_pago = db.query(PagPago).get(pag_pago_id)
    if pag_pago is None:
        raise CitasNotExistsError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise CitasIsDeletedError("No es activo ese pago, está eliminado")
    return pag_pago
