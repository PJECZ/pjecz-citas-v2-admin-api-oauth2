"""
Cit Dias Disponibles v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false

from .crud import get_cit_dias_disponibles, get_cit_dia_disponible
from .schemas import CitDiaDisponibleOut, OneCitDiaDisponibleOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_dias_disponibles = APIRouter(prefix="/v2/cit_dias_disponibles", tags=["citas dias disponibles"])


@cit_dias_disponibles.get("", response_model=CustomList[CitDiaDisponibleOut])
async def listado_dias_disponibles(
    db: Session = Depends(get_db),
    current_user: UsuarioInDB = Depends(get_current_active_user),
    settings: Settings = Depends(get_settings),
    size: int = 100,
):
    """Listado de dias disponibles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_dias_disponibles(
            db=db,
            settings=settings,
            size=size,
        )
    except CitasAnyError as error:
        return custom_list_success_false(error)
    items = [CitDiaDisponibleOut(fecha=item) for item in resultados]
    result = ListResult(total=len(items), items=items, size=size)
    return CustomList(result=result)


@cit_dias_disponibles.get("/proximo", response_model=OneCitDiaDisponibleOut)
async def proximo_dia_disponible(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Proximo dia disponible sin tomar en cuenta la hora"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    fecha = get_cit_dia_disponible(db=db)
    return OneCitDiaDisponibleOut(fecha=fecha)
