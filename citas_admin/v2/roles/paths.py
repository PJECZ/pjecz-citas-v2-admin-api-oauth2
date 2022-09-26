"""
Roles v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_roles, get_rol
from .schemas import RolOut, OneRolOut
from ..permisos.crud import get_permisos
from ..permisos.models import Permiso
from ..permisos.schemas import PermisoOut
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB
from ..usuarios_roles.crud import get_usuarios_roles
from ..usuarios_roles.schemas import UsuarioRolOut

roles = APIRouter(prefix="/v2/roles", tags=["usuarios"])


@roles.get("", response_model=CustomPage[RolOut])
async def listado_roles(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de roles"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_roles(
            db=db,
            estatus=estatus,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@roles.get("/{rol_id}", response_model=OneRolOut)
async def detalle_rol(
    rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una roles a partir de su id"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        rol = get_rol(
            db=db,
            rol_id=rol_id,
        )
    except CitasAnyError as error:
        return OneRolOut(success=False, message=str(error))
    return OneRolOut.from_orm(rol)


@roles.get("/{rol_id}/usuarios", response_model=CustomPage[UsuarioRolOut])
async def listado_usuarios_rol(
    rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios de un rol"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios_roles(
            db=db,
            rol_id=rol_id,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@roles.get("/{rol_id}/permisos", response_model=CustomPage[PermisoOut])
async def listado_permisos_rol(
    rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de permisos de un rol"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_permisos(
            db=db,
            rol_id=rol_id,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)
