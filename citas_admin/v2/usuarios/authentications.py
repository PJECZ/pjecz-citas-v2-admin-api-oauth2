"""
Authentications
"""
from datetime import datetime
from typing import Optional

from hashids import Hashids
from fastapi.security.api_key import APIKeyHeader
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from lib.database import get_db

from .models import Usuario
from .schemas import UsuarioInDB

X_API_KEY = APIKeyHeader(name="X-API-Key")


def get_user(
    usuario_id: int,
    db: Session = Depends(get_db),
) -> Optional[UsuarioInDB]:
    """Get user from email"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario:
        return UsuarioInDB(
            id=usuario.id,
            distrito_id=usuario.autoridad.distrito_id,
            distrito_nombre=usuario.autoridad.distrito.nombre,
            distrito_nombre_corto=usuario.autoridad.distrito.nombre_corto,
            autoridad_id=usuario.autoridad_id,
            autoridad_clave=usuario.autoridad.clave,
            autoridad_descripcion=usuario.autoridad.descripcion,
            autoridad_descripcion_corta=usuario.autoridad.descripcion_corta,
            oficina_id=usuario.oficina_id,
            oficina_clave=usuario.oficina.clave,
            oficina_descripcion=usuario.oficina.descripcion,
            oficina_descripcion_corta=usuario.oficina.descripcion_corta,
            email=usuario.email,
            nombres=usuario.nombres,
            apellido_paterno=usuario.apellido_paterno,
            apellido_materno=usuario.apellido_materno,
            curp=usuario.curp,
            puesto=usuario.puesto,
            telefono_celular=usuario.telefono_celular,
            api_key=usuario.api_key,
            api_key_expiracion=usuario.api_key_expiracion,
            username=usuario.email,
            permissions=usuario.permissions,
            hashed_password=usuario.contrasena,
            disabled=usuario.estatus != "A",
        )
    return None


def authenticate_user(
    api_key: str,
    db: Session = Depends(get_db),
) -> Optional[UsuarioInDB]:
    """Authenticate user"""

    # Separar el id, el email y la cadena aleatoria del api_key
    api_key_id, api_key_email, api_key_aleatorio = api_key.split(".")

    # Obtener el usuario
    usuario_id = Usuario.decode_id(api_key_id)
    if usuario_id is None:
        print("No se pudo decodificar el id")
        return False
    usuario = get_user(usuario_id, db)
    if usuario is None:
        print("No se encontró el usuario")
        return False

    # Validar el email hasheado
    if api_key_email != Hashids(salt=usuario.email, min_length=8).encode(1):
        print(f"El email no coincide {api_key_email}")
        return False

    # Validar el api_key
    if usuario.api_key != api_key:
        print(f"El api_key no coincide {usuario.api_key}")
        return False
    if usuario.api_key_expiracion < datetime.now():
        print("El api_key ha expirado")
        return False

    # Validad que sea activo
    if usuario.disabled:
        return False

    return usuario


async def get_current_active_user(
    api_key: str = Depends(X_API_KEY),
    db: Session = Depends(get_db),
):
    """Get current user"""
    usuario = authenticate_user(api_key, db)
    if usuario is False:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY")
    return usuario
