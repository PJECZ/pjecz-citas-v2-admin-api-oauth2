"""
Domicilios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Domicilio


def get_domicilios(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los domicilios activos"""
    consulta = db.query(Domicilio)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    return consulta.order_by(Domicilio.id)


def get_domicilio(
    db: Session,
    domicilio_id: int,
) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = db.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise CitasNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese domicilio, está eliminado")
    return domicilio
