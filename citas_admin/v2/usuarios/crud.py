"""
Usuarios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import Usuario
from ..autoridades.crud import get_autoridad
from ..oficinas.crud import get_oficina


def get_usuarios(
    db: Session,
    autoridad_id: int = None,
    oficina_id: int = None,
) -> Any:
    """Consultar los usuarios activos"""
    consulta = db.query(Usuario)
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(Usuario.oficina == oficina)
    return consulta.filter_by(estatus="A").order_by(Usuario.id)


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    """Consultar un usuario por su id"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        raise NotExistsException("No existe ese usuario")
    if usuario.estatus != "A":
        raise IsDeletedException("No es activo ese usuario, está eliminado")
    return usuario
