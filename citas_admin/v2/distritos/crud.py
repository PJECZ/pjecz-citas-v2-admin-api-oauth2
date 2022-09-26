"""
Distritos v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Distrito


def get_distritos(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los distritos activos"""
    consulta = db.query(Distrito)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    return consulta.order_by(Distrito.nombre)


def get_distrito(
    db: Session,
    distrito_id: int,
) -> Distrito:
    """Consultar un distrito por su id"""
    distrito = db.query(Distrito).get(distrito_id)
    if distrito is None:
        raise CitasNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise CitasIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito
