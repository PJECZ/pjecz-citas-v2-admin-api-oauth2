"""
Cit Horas Bloqueadas v2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import CitHoraBloqueada
from ..oficinas.crud import get_oficina


def get_cit_horas_bloqueadas(
    db: Session,
    oficina_id: int = None,
    fecha: date = None,
) -> Any:
    """Consultar las horas bloqueadas activas"""
    consulta = db.query(CitHoraBloqueada)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitHoraBloqueada.oficina == oficina)
    if fecha is not None:
        consulta = consulta.filter_by(fecha=fecha)
    return consulta.filter_by(estatus="A").filter(CitHoraBloqueada.fecha >= date.today()).order_by(CitHoraBloqueada.fecha, CitHoraBloqueada.inicio)


def get_cit_hora_bloqueada(db: Session, cit_hora_bloqueada_id: int) -> CitHoraBloqueada:
    """Consultar un hora bloqueada por su id"""
    cit_hora_bloqueada = db.query(CitHoraBloqueada).get(cit_hora_bloqueada_id)
    if cit_hora_bloqueada is None:
        raise CitasNotExistsError("No existe esa hora bloqueada")
    if cit_hora_bloqueada.estatus != "A":
        raise CitasIsDeletedError("No es activa esa hora bloqueada, está eliminada")
    return cit_hora_bloqueada
