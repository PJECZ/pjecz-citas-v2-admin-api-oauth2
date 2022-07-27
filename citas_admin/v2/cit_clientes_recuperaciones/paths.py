"""
Cit Clientes Recuperaciones v2, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_clientes_recuperaciones, get_cit_cliente_recuperacion
from .schemas import CitClienteRecuperacionOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_clientes_recuperaciones = APIRouter(prefix="/v2/cit_clientes_recuperaciones", tags=["citas"])


@cit_clientes_recuperaciones.get("", response_model=LimitOffsetPage[CitClienteRecuperacionOut])
async def listado_cit_clientes_recuperaciones(
    cit_cliente_id: int = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de recuperaciones de clientes"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_clientes_recuperaciones(
            db,
            cit_cliente_id=cit_cliente_id,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            ya_recuperado=ya_recuperado,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_clientes_recuperaciones.get("/{cit_cliente_recuperacion_id}", response_model=CitClienteRecuperacionOut)
async def detalle_cit_cliente_recuperacion(
    cit_cliente_recuperacion_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una recuperaciones de clientes a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_recuperacion = get_cit_cliente_recuperacion(
            db,
            cit_cliente_recuperacion_id=cit_cliente_recuperacion_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionOut.from_orm(cit_cliente_recuperacion)
