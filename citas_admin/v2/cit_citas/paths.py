"""
Cit Citas v2, rutas (paths)
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_citas, get_cit_cita
from .schemas import CitCitaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_citas = APIRouter(prefix="/v2/cit_citas", tags=["citas"])


@cit_citas.get("", response_model=LimitOffsetPage[CitCitaOut])
async def listado_cit_citas(
    cit_cliente_id: int = None,
    cit_servicio_id: int = None,
    oficina_id: int = None,
    inicio_desde: datetime = None,
    inicio_hasta: datetime = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de citas"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_citas(
            db,
            cit_cliente_id=cit_cliente_id,
            cit_servicio_id=cit_servicio_id,
            oficina_id=oficina_id,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_citas.get("/{cit_cita_id}", response_model=CitCitaOut)
async def detalle_cit_cita(
    cit_cita_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una citas a partir de su id"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = get_cit_cita(db, cit_cita_id=cit_cita_id)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitCitaOut.from_orm(cit_cita)
