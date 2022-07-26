"""
Cit Horas Bloqueadas v2, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_cit_horas_bloqueadas, get_cit_hora_bloqueada
from .schemas import CitHoraBloqueadaOut, OneCitHoraBloqueadaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_horas_bloqueadas = APIRouter(prefix="/v2/cit_horas_bloqueadas", tags=["citas horas bloqueadas"])


@cit_horas_bloqueadas.get("", response_model=CustomPage[CitHoraBloqueadaOut])
async def listado_horas_bloqueadas(
    estatus: str = None,
    fecha: date = None,
    oficina_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de horas bloqueadas"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_horas_bloqueadas(
            db=db,
            estatus=estatus,
            fecha=fecha,
            oficina_id=oficina_id,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_horas_bloqueadas.get("/{cit_hora_bloqueada_id}", response_model=OneCitHoraBloqueadaOut)
async def detalle_hora_bloqueada(
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
        return OneCitHoraBloqueadaOut(success=False, message=str(error))
    return OneCitHoraBloqueadaOut.from_orm(cit_hora_bloqueada)
