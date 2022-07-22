"""
Materias v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import Materia


def get_materias(db: Session) -> Any:
    """Consultar las materias activas"""
    return db.query(Materia).filter_by(estatus="A").order_by(Materia.nombre)


def get_materia(db: Session, materia_id: int) -> Materia:
    """Consultar un materia por su id"""
    materia = db.query(Materia).get(materia_id)
    if materia is None:
        raise NotExistsException("No existe esa materia")
    if materia.estatus != "A":
        raise IsDeletedException("No es activa esa materia, está eliminada")
    return materia
