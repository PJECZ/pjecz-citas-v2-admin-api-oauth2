"""
Cit Dias Disponibles v2, rutas (paths)
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError

from .crud import get_cit_dias_disponibles, get_cit_dia_disponible
from .schemas import CitDiaDisponibleOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_dias_disponibles = APIRouter(prefix="/v2/cit_dias_disponibles", tags=["citas"])


@cit_dias_disponibles.get("", response_model=List[CitDiaDisponibleOut])
async def listado_cit_dias_disponibles(
    limit: int = 40,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de dias disponibles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_dias_disponibles(db=db, limit=limit)
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return listado


@cit_dias_disponibles.get("/proximo", response_model=CitDiaDisponibleOut)
async def proximo_cit_dia_disponible(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Proximo dia disponible sin tomar en cuenta la hora"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        dia_disponible = get_cit_dia_disponible(db)
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return dia_disponible
