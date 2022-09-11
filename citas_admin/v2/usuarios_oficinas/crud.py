"""
Usuarios-Oficinas v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError

from .models import UsuarioOficina
from ..oficinas.crud import get_oficina
from ..usuarios.crud import get_usuario


def get_usuarios_oficinas(
    db: Session,
    oficina_id: int = None,
    usuario_id: int = None,
) -> Any:
    """Consultar los usuarios-oficinas activos"""
    consulta = db.query(UsuarioOficina)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(UsuarioOficina.oficina == oficina)
    if usuario_id is not None:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter(UsuarioOficina.usuario == usuario)
    return consulta.filter_by(estatus="A").order_by(UsuarioOficina.id)


def get_usuario_oficina(db: Session, usuario_oficina_id: int) -> UsuarioOficina:
    """Consultar un usuario-oficina por su id"""
    usuario_oficina = db.query(UsuarioOficina).get(usuario_oficina_id)
    if usuario_oficina is None:
        raise CitasNotExistsError("No existe ese usuario-oficina")
    if usuario_oficina.estatus != "A":
        raise CitasIsDeletedError("No es activo ese usuario-oficina, está eliminado")
    return usuario_oficina
