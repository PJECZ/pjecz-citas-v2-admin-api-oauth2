"""
Cit Citas Anonimas, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time
from typing import Any
from sqlalchemy.orm import Session

from ..oficinas.crud import get_oficina
from ..cit_citas.models import CitCita


def get_cit_citas_anonimas(db: Session, oficina_id: int, fecha: date = None, hora_minuto: time = None) -> Any:
    """Consultar las citas"""
    consulta = db.query(CitCita)

    # Filtrar por la oficina
    oficina = get_oficina(db, oficina_id)
    consulta = consulta.filter(CitCita.oficina == oficina)

    # Si se filtra por fecha
    if fecha is not None:
        inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=0, minute=0, second=0)
        termino_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.inicio >= inicio_dt).filter(CitCita.inicio <= termino_dt)

    # Si se filtra por hora_minuto
    if fecha is not None and hora_minuto is not None:
        inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute, second=0)
        consulta = consulta.filter(CitCita.inicio == inicio_dt)

    # Filtro por tiempo de termino
    hasta_tiempo = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=23,
        minute=59,
        second=59,
    )
    consulta = consulta.filter(CitCita.termino <= hasta_tiempo)

    # Descartar las citas canceladas
    consulta = consulta.filter(CitCita.estado != "CANCELO")

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCita.id)
