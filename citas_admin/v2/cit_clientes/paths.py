"""
Cit Clientes v2, rutas (paths)
"""
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_clientes, get_cit_cliente, get_cit_clientes_cantidades_creados_por_dia
from .schemas import CitClienteOut, CitClienteCantidadesCreadosPorDiaOut
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
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_clientes(db)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_clientes.get("/creados_por_dia", response_model=List[CitClienteCantidadesCreadosPorDiaOut])
async def listado_cit_clientes_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de cantidades de clientes creados por dia"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_cit_clientes_cantidades_creados_por_dia(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except OutOfRangeException as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return consulta.all()


@cit_clientes.get("/{cit_cliente_id}", response_model=CitClienteOut)
async def detalle_cit_cliente(
    cit_cliente_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una clientes a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente = get_cit_cliente(
            db,
            cit_cliente_id=cit_cliente_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteOut.from_orm(cit_cliente)
