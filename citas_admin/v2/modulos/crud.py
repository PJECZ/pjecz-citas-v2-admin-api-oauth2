"""
Modulos v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Modulo


def get_modulos(db: Session) -> Any:
    """Consultar los modulos activos"""
    consulta = db.query(Modulo)
    return consulta.filter_by(estatus="A").order_by(Modulo.nombre)


def get_modulo(db: Session, modulo_id: int) -> Modulo:
    """Consultar un modulo por su id"""
    modulo = db.query(Modulo).get(modulo_id)
    if modulo is None:
        raise CitasNotExistsError("No existe ese modulo")
    if modulo.estatus != "A":
        raise CitasIsDeletedError("No es activo ese modulo, está eliminado")
    return modulo
