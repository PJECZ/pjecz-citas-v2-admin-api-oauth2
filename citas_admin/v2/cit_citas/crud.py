"""
Cit Citas v2, CRUD (create, read, update, and delete)
"""
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitCita
from ..cit_clientes.crud import get_cit_cliente
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_citas(
    db: Session,
    cit_cliente_id: int = None,
    cit_servicio_id: int = None,
    oficina_id: int = None,
    inicio_desde: datetime = None,
    inicio_hasta: datetime = None,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(cit_cliente=cit_cliente)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(cit_servicio=cit_servicio)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(oficina=oficina)
    if inicio_desde is not None:
        consulta = consulta.filter(CitCita.inicio >= inicio_desde)
    if inicio_hasta is not None:
        consulta = consulta.filter(CitCita.inicio <= inicio_hasta)
    return consulta.filter_by(estatus="A").order_by(CitCita.id.desc())


def get_cit_cita(db: Session, cit_cita_id: int) -> CitCita:
    """Consultar un cita por su id"""
    cit_cita = db.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise NotExistsException("No existe ese cita")
    if cit_cita.estatus != "A":
        raise IsDeletedException("No es activo ese cita, está eliminado")
    return cit_cita
