"""
Cit Clientes v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, make_custom_error_page

from .crud import get_cit_clientes, get_cit_cliente, get_cit_clientes_creados_por_dia
from .schemas import CitClienteOut, CitClienteCreadosPorDiaOut, OneCitClienteOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_clientes = APIRouter(prefix="/v2/cit_clientes", tags=["citas clientes"])


@cit_clientes.get("", response_model=CustomPage[CitClienteOut])
async def listado_clientes(
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    enviar_boletin: bool = None,
    nombres: str = None,
    telefono: str = None,
    tiene_contrasena_sha256: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Listado de clientes"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes(
            db=db,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            curp=curp,
            email=email,
            enviar_boletin=enviar_boletin,
            nombres=nombres,
            telefono=telefono,
            tiene_contrasena_sha256=tiene_contrasena_sha256,
            settings=settings,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@cit_clientes.get("/creados_por_dia", response_model=CitClienteCreadosPorDiaOut)
async def cantidades_clientes_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Calcular cantidades de clientes creados por dia"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        fechas_cantidades = get_cit_clientes_creados_por_dia(
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
    return CitClienteCreadosPorDiaOut(items=fechas_cantidades, total=total)


@cit_clientes.get("/{cit_cliente_id}", response_model=OneCitClienteOut)
async def detalle_cliente(
    cit_cliente_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una clientes a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente = get_cit_cliente(
            db=db,
            cit_cliente_id=cit_cliente_id,
        )
    except CitasAnyError as error:
        return OneCitClienteOut(success=False, message=str(error))
    return OneCitClienteOut.from_orm(cit_cliente)
