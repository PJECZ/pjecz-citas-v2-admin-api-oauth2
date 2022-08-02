"""
Cit Clientes Recuperaciones v2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException
from lib.safe_string import safe_email

from .models import CitClienteRecuperacion
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente

HOY = date.today()
ANTIGUA_FECHA = date(year=2022, month=1, day=1)


def get_cit_clientes_recuperaciones(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    ya_recuperado: bool = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Consultar los recuperaciones activos"""
    consulta = db.query(CitClienteRecuperacion)
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, get_cit_cliente)
        consulta = consulta.filter(CitClienteRecuperacion.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=True)
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)
    if ya_recuperado is not None:
        consulta = consulta.filter_by(ya_recuperado=ya_recuperado)
    if creado_desde is not None:
        if not ANTIGUA_FECHA <= creado_desde <= HOY:
            raise OutOfRangeException("Creado desde fuera de rango")
        consulta = consulta.filter(func.date(CitClienteRecuperacion.creado) >= creado_desde)
    if creado_hasta is not None:
        if not ANTIGUA_FECHA <= creado_hasta <= HOY:
            raise OutOfRangeException("Creado hasta fuera de rango")
        consulta = consulta.filter(func.date(CitClienteRecuperacion.creado) <= creado_hasta)
    return consulta.filter_by(estatus="A").order_by(CitClienteRecuperacion.id)


def get_cit_cliente_recuperacion(db: Session, cit_cliente_recuperacion_id: int) -> CitClienteRecuperacion:
    """Consultar un recuperacion por su id"""
    cit_cliente_recuperacion = db.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if cit_cliente_recuperacion is None:
        raise NotExistsException("No existe ese recuperacion")
    if cit_cliente_recuperacion.estatus != "A":
        raise IsDeletedException("No es activo ese recuperacion, está eliminado")
    return cit_cliente_recuperacion
