"""
Cit Clientes Recuperaciones v2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitClienteRecuperacion
from ..cit_clientes.crud import get_cit_cliente


def get_cit_clientes_recuperaciones(
    db: Session,
    cit_cliente_id: int = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
) -> Any:
    """Consultar los recuperaciones activos"""
    consulta = db.query(CitClienteRecuperacion)
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, get_cit_cliente)
        consulta = consulta.filter(cit_cliente=cit_cliente)
    if creado_desde is not None:
        consulta = consulta.filter(CitClienteRecuperacion.creado >= creado_desde)
    if creado_hasta is not None:
        consulta = consulta.filter(CitClienteRecuperacion.creado <= creado_hasta)
    if ya_recuperado is not None:
        consulta = consulta.filter_by(ya_recuperado=ya_recuperado)
    return consulta.filter_by(estatus="A").order_by(CitClienteRecuperacion.id)


def get_cit_cliente_recuperacion(db: Session, cit_cliente_recuperacion_id: int) -> CitClienteRecuperacion:
    """Consultar un recuperacion por su id"""
    cit_cliente_recuperacion = db.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if cit_cliente_recuperacion is None:
        raise NotExistsException("No existe ese recuperacion")
    if cit_cliente_recuperacion.estatus != "A":
        raise IsDeletedException("No es activo ese recuperacion, está eliminado")
    return cit_cliente_recuperacion
