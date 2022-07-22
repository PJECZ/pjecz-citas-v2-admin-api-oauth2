"""
Autoridades v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_autoridades, get_autoridad
from .schemas import AutoridadOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

autoridades = APIRouter(prefix="/v2/autoridades", tags=["catalogos"])


@autoridades.get("", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades(
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=distrito_id,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@autoridades.get("/{autoridad_id}", response_model=AutoridadOut)
async def detalle_autoridad(
    autoridad_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridades a partir de su id"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        autoridad = get_autoridad(db, autoridad_id=autoridad_id)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut.from_orm(autoridad)
