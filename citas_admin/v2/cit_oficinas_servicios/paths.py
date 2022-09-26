"""
Cit Oficinas Servicios v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_cit_oficinas_servicios, get_cit_oficina_servicio
from .schemas import CitOficinaServicioOut, OneCitOficinaServicioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_oficinas_servicios = APIRouter(prefix="/v2/cit_oficinas_servicios", tags=["citas oficinas servicios"])


@cit_oficinas_servicios.get("", response_model=CustomPage[CitOficinaServicioOut])
async def listado_oficinas_servicios(
    cit_servicio_id: int = None,
    oficina_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas-servicios"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_oficinas_servicios(
            db=db,
            cit_servicio_id=cit_servicio_id,
            oficina_id=oficina_id,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_oficinas_servicios.get("/{cit_oficina_servicio_id}", response_model=OneCitOficinaServicioOut)
async def detalle_oficina_servicio(
    cit_oficina_servicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficinas-servicios a partir de su id"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_oficina_servicio = get_cit_oficina_servicio(
            db=db,
            cit_oficina_servicio_id=cit_oficina_servicio_id,
        )
    except CitasAnyError as error:
        return OneCitOficinaServicioOut(success=False, message=str(error))
    return OneCitOficinaServicioOut.from_orm(cit_oficina_servicio)
