"""
Distritos v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom import CustomPage, make_custom_error_page

from .crud import get_distritos, get_distrito
from .schemas import DistritoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

distritos = APIRouter(prefix="/v2/distritos", tags=["catalogos"])


@distritos.get("", response_model=CustomPage[DistritoOut])
async def listado_distritos(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de distritos"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_distritos(db=db)
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@distritos.get("/{distrito_id}", response_model=DistritoOut)
async def detalle_distrito(
    distrito_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una distritos a partir de su id"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        distrito = get_distrito(
            db=db,
            distrito_id=distrito_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return DistritoOut.from_orm(distrito)
