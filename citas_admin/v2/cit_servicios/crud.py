"""
Cit Servicios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import CitServicio
from ..cit_categorias.crud import get_cit_categoria


def get_cit_servicios(db: Session, cit_categoria_id: int = None) -> Any:
    """Consultar los servicios activos"""
    consulta = db.query(CitServicio)
    if cit_categoria_id is not None:
        cit_categoria = get_cit_categoria(db, cit_categoria_id)
        consulta = consulta.filter(CitServicio.cit_categoria == cit_categoria)
    return consulta.filter_by(estatus="A").order_by(CitServicio.clave)


def get_cit_servicio(db: Session, cit_servicio_id: int) -> CitServicio:
    """Consultar un servicio por su id"""
    cit_servicio = db.query(CitServicio).get(cit_servicio_id)
    if cit_servicio is None:
        raise CitasNotExistsError("No existe ese servicio")
    if cit_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese servicio, está eliminado")
    return cit_servicio
