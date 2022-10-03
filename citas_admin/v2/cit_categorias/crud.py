"""
Cit Categorias v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import CitCategoria


def get_cit_categorias(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar las categorias activas"""
    consulta = db.query(CitCategoria)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    return consulta.order_by(CitCategoria.nombre)


def get_cit_categoria(
    db: Session,
    cit_categoria_id: int,
) -> CitCategoria:
    """Consultar una categoria por su id"""
    cit_categoria = db.query(CitCategoria).get(cit_categoria_id)
    if cit_categoria is None:
        raise CitasNotExistsError("No existe esa categoria")
    if cit_categoria.estatus != "A":
        raise CitasIsDeletedError("No es activa esa categoria, está eliminada")
    return cit_categoria
