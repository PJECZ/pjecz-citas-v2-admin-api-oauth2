"""
Roles v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Rol


def get_roles(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los roles activos"""
    consulta = db.query(Rol)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    return consulta.order_by(Rol.nombre)


def get_rol(
    db: Session,
    rol_id: int,
) -> Rol:
    """Consultar un rol por su id"""
    rol = db.query(Rol).get(rol_id)
    if rol is None:
        raise CitasNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise CitasIsDeletedError("No es activo ese rol, está eliminado")
    return rol
