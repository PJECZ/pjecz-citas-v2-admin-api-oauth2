"""
Cit Servicios v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_cit_servicios, get_cit_servicio
from .schemas import CitServicioOut, OneCitServicioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_servicios = APIRouter(prefix="/v2/cit_servicios", tags=["citas servicios"])


@cit_servicios.get("", response_model=CustomPage[CitServicioOut])
async def listado_servicios(
    cit_categoria_id: int = None,
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de servicios"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_servicios(
            db=db,
            cit_categoria_id=cit_categoria_id,
            estatus=estatus,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_servicios.get("/{cit_servicio_id}", response_model=OneCitServicioOut)
async def detalle_servicio(
    cit_servicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una servicios a partir de su id"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_servicio = get_cit_servicio(
            db=db,
            cit_servicio_id=cit_servicio_id,
        )
    except CitasAnyError as error:
        return OneCitServicioOut(success=False, message=str(error))
    return OneCitServicioOut.from_orm(cit_servicio)
