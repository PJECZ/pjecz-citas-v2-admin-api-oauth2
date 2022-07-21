"""
Cit Categorias v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import CitCategoria


def get_cit_categorias(db: Session) -> Any:
    """Consultar las categorias activas"""
    return db.query(CitCategoria).filter_by(estatus="A").order_by(CitCategoria.nombre)


def get_cit_categoria(db: Session, cit_categoria_id: int) -> CitCategoria:
    """Consultar una categoria por su id"""
    cit_categoria = db.query(CitCategoria).get(cit_categoria_id)
    if cit_categoria is None:
        raise NotExistsException("No existe esa categoria")
    if cit_categoria.estatus != "A":
        raise IsDeletedException("No es activa esa categoria, está eliminada")
    return cit_categoria
