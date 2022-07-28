"""
Cit Clientes Registros v2, rutas (paths)
"""
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_clientes_registros, get_cit_cliente_registro, get_cit_clientes_registros_cantidades_creados_por_dia
from .schemas import CitClienteRegistroOut, CitClienteRegistroCantidadesCreadasPorDiaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_clientes_registros = APIRouter(prefix="/v2/cit_clientes_registros", tags=["citas"])


@cit_clientes_registros.get("", response_model=LimitOffsetPage[CitClienteRegistroOut])
async def listado_cit_clientes_registros(
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_registrado: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de registros de clientes"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_clientes_registros(
            db,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            ya_registrado=ya_registrado,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_clientes_registros.get("/creados_por_dia", response_model=List[CitClienteRegistroCantidadesCreadasPorDiaOut])
async def listado_cit_clientes_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de cantidades de registros de clientes creados por dia"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_cit_clientes_registros_cantidades_creados_por_dia(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except OutOfRangeException as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return consulta.all()


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=CitClienteRegistroOut)
async def detalle_cit_cliente_registro(
    cit_cliente_registro_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una registros de clientes a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_registro = get_cit_cliente_registro(
            db,
            cit_cliente_registro_id=cit_cliente_registro_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroOut.from_orm(cit_cliente_registro)
