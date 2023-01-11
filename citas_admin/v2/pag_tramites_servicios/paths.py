"""
Pagos Tramites y Servicios v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_pag_tramites_servicios, get_pag_tramite_servicio
from .schemas import PagTramiteServicioOut, OnePagTramiteServicioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

pag_tramites_servicios = APIRouter(prefix="/v2/pag_tramites_servicios", tags=["pagos"])


@pag_tramites_servicios.get("", response_model=CustomPage[PagTramiteServicioOut])
async def listado_pag_tramites_servicios(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tramites y servicios"""
    if current_user.permissions.get("PAG TRAMITES SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_pag_tramites_servicios(
            db=db,
            estatus=estatus,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@pag_tramites_servicios.get("/{pag_tramite_servicio_id}", response_model=OnePagTramiteServicioOut)
async def detalle_pag_tramite_servicio(
    pag_tramite_servicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una tramites y servicios a partir de su id"""
    if current_user.permissions.get("PAG TRAMITES SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        pag_tramite_servicio = get_pag_tramite_servicio(
            db=db,
            pag_tramite_servicio_id=pag_tramite_servicio_id,
        )
    except CitasAnyError as error:
        return OnePagTramiteServicioOut(success=False, message=str(error))
    return OnePagTramiteServicioOut.from_orm(pag_tramite_servicio)
