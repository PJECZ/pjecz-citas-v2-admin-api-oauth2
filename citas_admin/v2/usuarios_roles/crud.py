"""
Usuarios-Roles v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import UsuarioRol
from ..roles.crud import get_rol
from ..usuarios.crud import get_usuario


def get_usuarios_roles(
    db: Session,
    estatus: str = None,
    rol_id: int = None,
    usuario_id: int = None,
) -> Any:
    """Consultar los usuarios-roles activos"""
    consulta = db.query(UsuarioRol)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    if rol_id is not None:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(UsuarioRol.rol == rol)
    if usuario_id is not None:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter(UsuarioRol.usuario == usuario)
    return consulta.order_by(UsuarioRol.id)


def get_usuario_rol(
    db: Session,
    usuario_rol_id: int,
) -> UsuarioRol:
    """Consultar un usuario-rol por su id"""
    usuario_rol = db.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        raise CitasNotExistsError("No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        raise CitasIsDeletedError("No es activo ese usuario-rol, está eliminado")
    return usuario_rol
