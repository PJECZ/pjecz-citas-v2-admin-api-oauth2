"""
Cit Clientes Registros v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_clientes_registros, get_cit_cliente_registro, get_cit_clientes_registros_creados_por_dia
from .schemas import CitClienteRegistroOut, CitClientesRegistrosCreadosPorDiaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_clientes_registros = APIRouter(prefix="/v2/cit_clientes_registros", tags=["citas clientes registros"])


@cit_clientes_registros.get("", response_model=LimitOffsetPage[CitClienteRegistroOut])
async def listado_cit_clientes_registros(
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    ya_registrado: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de registros de clientes"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultado = get_cit_clientes_registros(
            db=db,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            curp=curp,
            email=email,
            nombres=nombres,
            ya_registrado=ya_registrado,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(resultado)


@cit_clientes_registros.get("/creados_por_dia", response_model=CitClientesRegistrosCreadosPorDiaOut)
async def calcular_cantidades_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Calcular las cantidades de registros de clientes creados por dia"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        fechas_cantidades = get_cit_clientes_registros_creados_por_dia(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    total = 0
    for fecha_cantidad in fechas_cantidades:
        total += fecha_cantidad["cantidad"]
    return CitClientesRegistrosCreadosPorDiaOut(items=fechas_cantidades, total=total)


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
            db=db,
            cit_cliente_registro_id=cit_cliente_registro_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroOut.from_orm(cit_cliente_registro)
