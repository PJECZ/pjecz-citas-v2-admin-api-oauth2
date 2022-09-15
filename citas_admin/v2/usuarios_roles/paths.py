"""
Usuarios-Roles v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, make_custom_error_page

from .crud import get_usuarios_roles, get_usuario_rol
from .schemas import UsuarioRolOut, OneUsuarioRolOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

usuarios_roles = APIRouter(prefix="/v2/usuarios_roles", tags=["usuarios"])


@usuarios_roles.get("", response_model=CustomPage[UsuarioRolOut])
async def listado_usuarios_roles(
    rol_id: int = None,
    usuario_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios-roles"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios_roles(
            db=db,
            rol_id=rol_id,
            usuario_id=usuario_id,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@usuarios_roles.get("/{usuario_rol_id}", response_model=OneUsuarioRolOut)
async def detalle_usuario_rol(
    usuario_rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una usuarios-roles a partir de su id"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_rol = get_usuario_rol(
            db=db,
            usuario_rol_id=usuario_rol_id,
        )
    except CitasAnyError as error:
        return OneUsuarioRolOut(success=False, message=str(error))
    return OneUsuarioRolOut.from_orm(usuario_rol)
