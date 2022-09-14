"""
Cit Clientes Recuperaciones v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom import CustomPage, make_custom_error_page

from .crud import get_cit_clientes_recuperaciones, get_cit_cliente_recuperacion, get_cit_clientes_recuperaciones_creados_por_dia
from .schemas import CitClienteRecuperacionOut, CitClientesRecuperacionesCreadosPorDiaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_clientes_recuperaciones = APIRouter(prefix="/v2/cit_clientes_recuperaciones", tags=["citas clientes recuperaciones"])


@cit_clientes_recuperaciones.get("", response_model=CustomPage[CitClienteRecuperacionOut])
async def listar_recuperaciones(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Listado de recuperaciones de clientes"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes_recuperaciones(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            ya_recuperado=ya_recuperado,
            settings=settings,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@cit_clientes_recuperaciones.get("/creados_por_dia", response_model=CitClientesRecuperacionesCreadosPorDiaOut)
async def cantidades_recuperaciones_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Calcular cantidades de clientes creados por dia"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        fechas_cantidades = get_cit_clientes_recuperaciones_creados_por_dia(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            settings=settings,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    total = 0
    for fecha_cantidad in fechas_cantidades:
        total += fecha_cantidad["cantidad"]
    return CitClientesRecuperacionesCreadosPorDiaOut(items=fechas_cantidades, total=total)


@cit_clientes_recuperaciones.get("/{cit_cliente_recuperacion_id}", response_model=CitClienteRecuperacionOut)
async def detalle_recuperacion(
    cit_cliente_recuperacion_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una recuperaciones de clientes a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_recuperacion = get_cit_cliente_recuperacion(
            db=db,
            cit_cliente_recuperacion_id=cit_cliente_recuperacion_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionOut.from_orm(cit_cliente_recuperacion)
