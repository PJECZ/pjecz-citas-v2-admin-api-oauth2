"""
Cit Horas Disponibles v2, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_horas_disponibles
from .schemas import CitHoraDisponibleOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_horas_disponibles = APIRouter(prefix="/v2/cit_horas_disponibles", tags=["horas disponibles"])


@cit_horas_disponibles.get("", response_model=LimitOffsetPage[CitHoraDisponibleOut])
async def listado_cit_horas_disponibles(
    cit_servicio_id: int,
    fecha: date,
    oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Listado de horas disponibles"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_horas_disponibles(
            db=db,
            cit_servicio_id=cit_servicio_id,
            oficina_id=oficina_id,
            fecha=fecha,
            settings=settings,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
