"""
Usuarios v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_usuarios, get_usuario
from .schemas import UsuarioOut, OneUsuarioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

usuarios = APIRouter(prefix="/v2/usuarios", tags=["usuarios"])


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def listado_usuarios(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    estatus: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios(
            db=db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            estatus=estatus,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@usuarios.get("/{usuario_id}", response_model=OneUsuarioOut)
async def detalle_usuario(
    usuario_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una usuarios a partir de su id"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario = get_usuario(
            db=db,
            usuario_id=usuario_id,
        )
    except CitasAnyError as error:
        return OneUsuarioOut(success=False, message=str(error))
    return OneUsuarioOut.from_orm(usuario)
