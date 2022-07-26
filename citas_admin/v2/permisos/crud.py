"""
Permisos v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import Permiso
from ..modulos.crud import get_modulo
from ..roles.crud import get_rol


def get_permisos(
    db: Session,
    estatus: str = None,
    modulo_id: int = None,
    rol_id: int = None,
) -> Any:
    """Consultar los permisos activos"""
    consulta = db.query(Permiso)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    if modulo_id is not None:
        modulo = get_modulo(db, modulo_id)
        consulta = consulta.filter(Permiso.modulo == modulo)
    if rol_id is not None:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(Permiso.rol == rol)
    return consulta.order_by(Permiso.id)


def get_permiso(db: Session, permiso_id: int) -> Permiso:
    """Consultar un permiso por su id"""
    permiso = db.query(Permiso).get(permiso_id)
    if permiso is None:
        raise CitasNotExistsError("No existe ese permiso")
    if permiso.estatus != "A":
        raise CitasIsDeletedError("No es activo ese permiso, está eliminado")
    return permiso
