"""
Cit Dias Inhabiles v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_dias_inhabiles, get_cit_dia_inhabil
from .schemas import CitDiaInhabilOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_dias_inhabiles = APIRouter(prefix="/v2/cit_dias_inhabiles", tags=["citas dias inhabiles"])


@cit_dias_inhabiles.get("", response_model=LimitOffsetPage[CitDiaInhabilOut])
async def listado_cit_dias_inhabiles(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de dias inhabiles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_dias_inhabiles(db=db)
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_dias_inhabiles.get("/{cit_dia_inhabil_id}", response_model=CitDiaInhabilOut)
async def detalle_dia_inhabil(
    cit_dia_inhabil_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una dias inhabiles a partir de su id"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        dia_inhabil = get_cit_dia_inhabil(
            db=db,
            cit_dia_inhabil_id=cit_dia_inhabil_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitDiaInhabilOut.from_orm(dia_inhabil)
