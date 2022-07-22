"""
Cit Clientes v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_clientes, get_cit_cliente
from .schemas import CitClienteOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_clientes = APIRouter(prefix="/v2/cit_clientes", tags=["citas"])


@cit_clientes.get("", response_model=LimitOffsetPage[CitClienteOut])
async def listado_cit_clientes(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de clientes"""
    if "CIT CLIENTES" not in current_user.permissions or current_user.permissions["CIT CLIENTES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_clientes(db)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_clientes.get("/{cit_cliente_id}", response_model=CitClienteOut)
async def detalle_cit_cliente(
    cit_cliente_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una clientes a partir de su id"""
    if "CIT CLIENTES" not in current_user.permissions or current_user.permissions["CIT CLIENTES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteOut.from_orm(cit_cliente)
