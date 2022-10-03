"""
Cit Dias Inhabiles v2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import CitDiaInhabil


def get_cit_dias_inhabiles(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los dias inhabiles activos, desde hoy"""
    consulta = db.query(CitDiaInhabil)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    consulta = consulta.filter(CitDiaInhabil.fecha >= date.today())  # Solo los dias de hoy en adelante
    return consulta.order_by(CitDiaInhabil.fecha)


def get_cit_dia_inhabil(
    db: Session,
    cit_dia_inhabil_id: int,
) -> CitDiaInhabil:
    """Consultar un dia inhabil por su id"""
    cit_dia_inhabil = db.query(CitDiaInhabil).get(cit_dia_inhabil_id)
    if cit_dia_inhabil is None:
        raise CitasNotExistsError("No existe ese dia inhabil")
    if cit_dia_inhabil.estatus != "A":
        raise CitasIsDeletedError("No es activo ese dia inhabil, está eliminado")
    return cit_dia_inhabil
