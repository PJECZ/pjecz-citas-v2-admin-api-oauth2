"""
Oficinas v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Oficina
from ..distritos.crud import get_distrito
from ..domicilios.crud import get_domicilio


def get_oficinas(
    db: Session,
    distrito_id: int = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    puede_agendar_citas: bool = None,
) -> Any:
    """Consultar los oficinas activos"""
    consulta = db.query(Oficina)
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Oficina.distrito == distrito)
    if domicilio_id is not None:
        domicilio = get_domicilio(db, domicilio_id)
        consulta = consulta.filter(Oficina.domicilio == domicilio)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    if puede_agendar_citas is not None:
        consulta = consulta.filter_by(puede_agendar_citas=puede_agendar_citas)
    return consulta.filter_by(estatus="A").order_by(Oficina.clave)


def get_oficina(db: Session, oficina_id: int) -> Oficina:
    """Consultar un oficina por su id"""
    oficina = db.query(Oficina).get(oficina_id)
    if oficina is None:
        raise CitasNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise CitasIsDeletedError("No es activo ese oficina, está eliminado")
    return oficina
