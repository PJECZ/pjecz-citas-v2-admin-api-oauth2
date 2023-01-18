"""
Pagos Tramites y Servicios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave

from .models import PagTramiteServicio


def get_pag_tramites_servicios(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los tramites y servicios activos"""

    # Consulta
    consulta = db.query(PagTramiteServicio)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(PagTramiteServicio.clave)


def get_pag_tramite_servicio(db: Session, pag_tramite_servicio_id: int) -> PagTramiteServicio:
    """Consultar un tramite y servicio por su id"""
    pag_tramite_servicio = db.query(PagTramiteServicio).get(pag_tramite_servicio_id)
    if pag_tramite_servicio is None:
        raise CitasNotExistsError("No existe ese tramite y servicio")
    if pag_tramite_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese tramite y servicio, está eliminado")
    return pag_tramite_servicio


def get_pag_tramite_servicio_from_clave(db: Session, clave: str) -> PagTramiteServicio:
    """Consultar un tramite y servicio por su clave"""
    clave = safe_clave(clave)
    if clave is None or clave == "":
        raise CitasNotValidParamError("No es válida la clave del tramite y servicio")
    pag_tramite_servicio = db.query(PagTramiteServicio).filter_by(clave=clave).first()
    if pag_tramite_servicio is None:
        raise CitasNotExistsError("No existe ese tramite y servicio")
    if pag_tramite_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese tramite y servicio, está eliminado")
    return pag_tramite_servicio
