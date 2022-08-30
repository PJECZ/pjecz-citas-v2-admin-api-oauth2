"""
Cit Horas Bloqueadas v2, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_horas_bloqueadas, get_cit_hora_bloqueada
from .schemas import CitHoraBloqueadaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_horas_bloqueadas = APIRouter(prefix="/v2/cit_horas_bloqueadas", tags=["citas"])


@cit_horas_bloqueadas.get("", response_model=LimitOffsetPage[CitHoraBloqueadaOut])
async def listado_cit_horas_bloqueadas(
    oficina_id: int = None,
    fecha: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de horas bloqueadas"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_horas_bloqueadas(
            db=db,
            oficina_id=oficina_id,
            fecha=fecha,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_horas_bloqueadas.get("/{cit_hora_bloqueada_id}", response_model=CitHoraBloqueadaOut)
async def detalle_cit_hora_bloqueada(
    cit_hora_bloqueada_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una horas bloqueadas a partir de su id"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_hora_bloqueada = get_cit_hora_bloqueada(
            db=db,
            cit_hora_bloqueada_id=cit_hora_bloqueada_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitHoraBloqueadaOut.from_orm(cit_hora_bloqueada)
