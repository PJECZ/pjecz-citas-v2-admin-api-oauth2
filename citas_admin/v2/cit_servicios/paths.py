"""
Cit Servicios v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom import CustomPage, make_custom_error_page

from .crud import get_cit_servicios, get_cit_servicio
from .schemas import CitServicioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_servicios = APIRouter(prefix="/v2/cit_servicios", tags=["citas servicios"])


@cit_servicios.get("", response_model=CustomPage[CitServicioOut])
async def listado_servicios(
    cit_categoria_id: int = None,
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
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@cit_servicios.get("/{cit_servicio_id}", response_model=CitServicioOut)
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
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitServicioOut.from_orm(cit_servicio)
