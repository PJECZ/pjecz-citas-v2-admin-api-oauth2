"""
Autoridades v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom import CustomPage, make_custom_error_page

from .crud import get_autoridades, get_autoridad
from .schemas import AutoridadOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

autoridades = APIRouter(prefix="/v2/autoridades", tags=["catalogos"])


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def listado_autoridades(
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_autoridades(
            db=db,
            distrito_id=distrito_id,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@autoridades.get("/{autoridad_id}", response_model=AutoridadOut)
async def detalle_autoridad(
    autoridad_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridades a partir de su id"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        autoridad = get_autoridad(
            db=db,
            autoridad_id=autoridad_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut.from_orm(autoridad)
