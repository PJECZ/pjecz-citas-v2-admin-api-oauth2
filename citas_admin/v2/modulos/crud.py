"""
Modulos v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import Modulo


def get_modulos(
    db: Session,
    en_navegacion: bool = None,
) -> Any:
    """Consultar los modulos activos"""
    consulta = db.query(Modulo)
    if en_navegacion is not None:
        consulta = consulta.filter_by(en_navegacion=en_navegacion)
    return consulta.filter_by(estatus="A").order_by(Modulo.nombre)


def get_modulo(db: Session, modulo_id: int) -> Modulo:
    """Consultar un modulo por su id"""
    modulo = db.query(Modulo).get(modulo_id)
    if modulo is None:
        raise NotExistsException("No existe ese modulo")
    if modulo.estatus != "A":
        raise IsDeletedException("No es activo ese modulo, está eliminado")
    return modulo
