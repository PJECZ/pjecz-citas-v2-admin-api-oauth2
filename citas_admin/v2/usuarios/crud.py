"""
Usuarios v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_email

from .models import Usuario
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave
from ..oficinas.crud import get_oficina, get_oficina_with_clave


def get_usuarios(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar los usuarios activos"""
    consulta = db.query(Usuario)
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(Usuario.oficina == oficina)
    elif oficina_clave is not None:
        oficina = get_oficina_with_clave(db, oficina_clave)
        consulta = consulta.filter(Usuario.oficina == oficina)
    return consulta.filter_by(estatus="A").order_by(Usuario.id.desc())


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    """Consultar un usuario por su id"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        raise CitasNotExistsError("No existe ese usuario")
    if usuario.estatus != "A":
        raise CitasIsDeletedError("No es activo ese usuario, está eliminado")
    return usuario


def get_usuario_with_email(db: Session, email: str) -> Usuario:
    """Consultar un usuario por su id"""
    email = safe_email(email)
    if email is None or email == "":
        raise CitasNotValidParamError("El email no es válido")
    usuario = db.query(Usuario).filter_by(email=email).first()
    if usuario is None:
        raise CitasNotExistsError("No existe ese usuario")
    if usuario.estatus != "A":
        raise CitasIsDeletedError("No es activo ese usuario, está eliminado")
    return usuario
