"""
Cit Oficinas-Servicios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import CitOficinaServicio
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_oficinas_servicios(
    db: Session,
    cit_servicio_id: int = None,
    estatus: str = None,
    oficina_id: int = None,
) -> Any:
    """Consultar las oficinas-servicios activas"""
    consulta = db.query(CitOficinaServicio)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitOficinaServicio.cit_servicio == cit_servicio)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitOficinaServicio.oficina == oficina)
    return consulta.order_by(CitOficinaServicio.id)


def get_cit_oficina_servicio(
    db: Session,
    cit_oficina_servicio_id: int,
) -> CitOficinaServicio:
    """Consultar una oficina-servicio por su id"""
    cit_oficina_servicio = db.query(CitOficinaServicio).get(cit_oficina_servicio_id)
    if cit_oficina_servicio is None:
        raise CitasNotExistsError("No existe esa oficina-servicio")
    if cit_oficina_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activa ese oficina-servicio, está eliminada")
    return cit_oficina_servicio
