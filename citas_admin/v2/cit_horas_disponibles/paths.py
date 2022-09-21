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
from lib.fastapi_pagination_custom_list import CustomList, ListResult, make_custom_error_list

from .crud import get_cit_horas_disponibles
from .schemas import CitHoraDisponibleOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_horas_disponibles = APIRouter(prefix="/v2/cit_horas_disponibles", tags=["citas horas disponibles"])


@cit_horas_disponibles.get("", response_model=CustomList[CitHoraDisponibleOut])
async def listado_cit_horas_disponibles(
    cit_servicio_id: int,
    fecha: date,
    oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    size: int = 90,
):
    """Listado de horas disponibles"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_horas_disponibles(
            db=db,
            cit_servicio_id=cit_servicio_id,
            oficina_id=oficina_id,
            fecha=fecha,
            settings=settings,
            size=size,
        )
    except CitasAnyError as error:
        return make_custom_error_list(error)
    items = [CitHoraDisponibleOut(horas_minutos=item) for item in resultados]
    result = ListResult(total=len(items), items=items, size=size)
    return CustomList(result=result)
