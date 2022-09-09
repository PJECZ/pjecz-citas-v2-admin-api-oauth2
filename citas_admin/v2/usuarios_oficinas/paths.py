"""
Usuarios-Oficinas v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_usuarios_oficinas, get_usuario_oficina
from .schemas import UsuarioOficinaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

usuarios_oficinas = APIRouter(prefix="/v2/usuarios_oficinas", tags=["usuarios"])


@usuarios_oficinas.get("", response_model=LimitOffsetPage[UsuarioOficinaOut])
async def listado_usuarios_oficinas(
    oficina_id: int = None,
    usuario_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios-oficinas"""
    if current_user.permissions.get("USUARIO OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_usuarios_oficinas(
            db=db,
            oficina_id=oficina_id,
            usuario_id=usuario_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@usuarios_oficinas.get("/{usuario_oficina_id}", response_model=UsuarioOficinaOut)
async def detalle_usuario_oficina(
    usuario_oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una usuarios-oficinas a partir de su id"""
    if current_user.permissions.get("USUARIO OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_oficina = get_usuario_oficina(db, usuario_oficina_id=usuario_oficina_id)
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return UsuarioOficinaOut.from_orm(usuario_oficina)