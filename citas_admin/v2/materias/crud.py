"""
Materias v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Materia


def get_materias(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar las materias activas"""
    consulta = db.query(Materia)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    return consulta.order_by(Materia.nombre)


def get_materia(
    db: Session,
    materia_id: int,
) -> Materia:
    """Consultar un materia por su id"""
    materia = db.query(Materia).get(materia_id)
    if materia is None:
        raise CitasNotExistsError("No existe esa materia")
    if materia.estatus != "A":
        raise CitasIsDeletedError("No es activa esa materia, está eliminada")
    return materia
