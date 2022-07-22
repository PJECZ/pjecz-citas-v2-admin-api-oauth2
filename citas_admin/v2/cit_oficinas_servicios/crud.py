"""
Cit Oficinas-Servicios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitOficinaServicio
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_oficinas_servicios(
    db: Session,
    cit_servicio_id: int = None,
    oficina_id: int = None,
) -> Any:
    """Consultar las oficinas-servicios activas"""
    consulta = db.query(CitOficinaServicio)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitOficinaServicio.cit_servicio == cit_servicio)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitOficinaServicio.oficina == oficina)
    return consulta.filter_by(estatus="A").order_by(CitOficinaServicio.id)


def get_cit_oficina_servicio(db: Session, cit_oficina_servicio_id: int) -> CitOficinaServicio:
    """Consultar una oficina-servicio por su id"""
    cit_oficina_servicio = db.query(CitOficinaServicio).get(cit_oficina_servicio_id)
    if cit_oficina_servicio is None:
        raise NotExistsException("No existe esa oficina-servicio")
    if cit_oficina_servicio.estatus != "A":
        raise IsDeletedException("No es activa ese oficina-servicio, está eliminada")
    return cit_oficina_servicio
