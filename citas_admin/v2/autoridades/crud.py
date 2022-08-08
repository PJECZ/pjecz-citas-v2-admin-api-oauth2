"""
Autoridades v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave

from .models import Autoridad
from ..distritos.crud import get_distrito


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
) -> Any:
    """Consultar las autoridades activas"""
    consulta = db.query(Autoridad)
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Autoridad.distrito == distrito)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    if es_notaria is not None:
        consulta = consulta.filter_by(es_notaria=es_notaria)
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave)


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar una autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise CitasNotExistsError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise CitasIsDeletedError("No es activa esa autoridad, está eliminada")
    return autoridad


def get_autoridad_with_clave(db: Session, clave: str) -> Autoridad:
    """Consultar una autoridad por su clave"""
    clave = safe_clave(clave)
    if clave is None:
        raise CitasNotValidParamError("La clave no es válida")
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise CitasNotExistsError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise CitasIsDeletedError("No es activa esa autoridad, está eliminada")
    return autoridad
