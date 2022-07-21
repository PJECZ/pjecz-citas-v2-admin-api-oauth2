"""
Cit Clientes v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitCliente


def get_cit_clientes(db: Session) -> Any:
    """Consultar los clientes activos"""
    return db.query(CitCliente).filter_by(estatus="A").order_by(CitCliente.id.desc())


def get_cit_cliente(db: Session, cit_cliente_id: int) -> CitCliente:
    """Consultar un cliente por su id"""
    cit_cliente = db.query(CitCliente).get(cit_cliente_id)
    if cit_cliente is None:
        raise NotExistsException("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise IsDeletedException("No es activo ese cliente, está eliminado")
    return cit_cliente
