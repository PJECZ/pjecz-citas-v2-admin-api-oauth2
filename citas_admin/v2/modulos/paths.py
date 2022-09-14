"""
Modulos v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom import CustomPage, make_custom_error_page

from .crud import get_modulos, get_modulo
from .schemas import ModuloOut, OneModuloOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

modulos = APIRouter(prefix="/v2/modulos", tags=["usuarios"])


@modulos.get("", response_model=CustomPage[ModuloOut])
async def listado_modulos(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de modulos"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_modulos(db=db)
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@modulos.get("/{modulo_id}", response_model=OneModuloOut)
async def detalle_modulo(
    modulo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una modulos a partir de su id"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        modulo = get_modulo(
            db=db,
            modulo_id=modulo_id,
        )
    except CitasAnyError as error:
        return OneModuloOut(success=False, message=str(error))
    return OneModuloOut.from_orm(modulo)
