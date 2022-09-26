"""
Autoridades v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave

from .models import Autoridad
from ..distritos.crud import get_distrito
from ..materias.crud import get_materia


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    estatus: str = None,
    materia_id: int = None,
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
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    if materia_id:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter(Autoridad.materia == materia)
    return consulta.order_by(Autoridad.clave)


def get_autoridad(
    db: Session,
    autoridad_id: int,
) -> Autoridad:
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
    if clave is None or clave == "":
        raise CitasNotValidParamError("No es válida la clave de la autoridad")
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise CitasNotExistsError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise CitasIsDeletedError("No es activa esa autoridad, está eliminada")
    return autoridad
