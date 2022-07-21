"""
Cit Clientes Registros v2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitClienteRegistro


def get_cit_clientes_registros(
    db: Session,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_registrado: bool = None,
) -> Any:
    """Consultar los registros de clientes activos"""
    consulta = db.query(CitClienteRegistro)
    if creado_desde is not None:
        consulta = consulta.filter(CitClienteRegistro.creado >= creado_desde)
    if creado_hasta is not None:
        consulta = consulta.filter(CitClienteRegistro.creado <= creado_hasta)
    if ya_registrado is not None:
        consulta = consulta.filter_by(ya_registrado=ya_registrado)
    return consulta.filter_by(estatus="A").order_by(CitClienteRegistro.id)


def get_cit_cliente_registro(db: Session, cit_cliente_registro_id: int) -> CitClienteRegistro:
    """Consultar un registro de cliente por su id"""
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise NotExistsException("No existe ese registro de cliente")
    if cit_cliente_registro.estatus != "A":
        raise IsDeletedException("No es activo ese registro de cliente, está eliminado")
    return cit_cliente_registro
