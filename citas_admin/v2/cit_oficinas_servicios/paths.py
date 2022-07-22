"""
Cit Oficinas Servicios v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_oficinas_servicios, get_cit_oficina_servicio
from .schemas import CitOficinaServicioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_oficinas_servicios = APIRouter(prefix="/v2/cit_oficinas_servicios", tags=["citas"])


@cit_oficinas_servicios.get("", response_model=LimitOffsetPage[CitOficinaServicioOut])
async def listado_cit_oficinas_servicios(
    cit_servicio_id: int = None,
    oficina_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas-servicios"""
    if "CIT OFICINAS SERVICIOS" not in current_user.permissions or current_user.permissions["CIT OFICINAS SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_oficinas_servicios(
            db,
            cit_servicio_id=cit_servicio_id,
            oficina_id=oficina_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_oficinas_servicios.get("/{cit_oficina_servicio_id}", response_model=CitOficinaServicioOut)
async def detalle_cit_oficina_servicio(
    cit_oficina_servicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficinas-servicios a partir de su id"""
    if "CIT OFICINAS SERVICIOS" not in current_user.permissions or current_user.permissions["CIT OFICINAS SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_oficina_servicio = get_cit_oficina_servicio(db, cit_oficina_servicio_id=cit_oficina_servicio_id)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitOficinaServicioOut.from_orm(cit_oficina_servicio)
