"""
Cit Dias Inhabiles v2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitDiaInhabil


def get_cit_dias_inhabiles(db: Session) -> Any:
    """Consultar los dias inhabiles activos, desde hoy"""
    return db.query(CitDiaInhabil).filter_by(estatus="A").filter(CitDiaInhabil.fecha >= date.today()).order_by(CitDiaInhabil.fecha)


def get_cit_dia_inhabil(db: Session, cit_dia_inhabil_id: int) -> CitDiaInhabil:
    """Consultar un dia inhabil por su id"""
    cit_dia_inhabil = db.query(CitDiaInhabil).get(cit_dia_inhabil_id)
    if cit_dia_inhabil is None:
        raise NotExistsException("No existe ese dia inhabil")
    if cit_dia_inhabil.estatus != "A":
        raise IsDeletedException("No es activo ese dia inhabil, está eliminado")
    return cit_dia_inhabil
