"""
Permisos v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom import CustomPage, make_custom_error_page

from .crud import get_permisos, get_permiso
from .schemas import PermisoOut, OnePermisoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

permisos = APIRouter(prefix="/v2/permisos", tags=["usuarios"])


@permisos.get("", response_model=CustomPage[PermisoOut])
async def listado_permisos(
    modulo_id: int = None,
    rol_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de permisos"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_permisos(
            db=db,
            modulo_id=modulo_id,
            rol_id=rol_id,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@permisos.get("/{permiso_id}", response_model=OnePermisoOut)
async def detalle_permiso(
    permiso_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una permisos a partir de su id"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        permiso = get_permiso(
            db=db,
            permiso_id=permiso_id,
        )
    except CitasAnyError as error:
        return OnePermisoOut(success=False, message=str(error))
    return OnePermisoOut.from_orm(permiso)
