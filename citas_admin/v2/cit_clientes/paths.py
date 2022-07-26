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
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false

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
    autoriza_mensajes: bool = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    enviar_boletin: bool = None,
    estatus: str = None,
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
            autoriza_mensajes=autoriza_mensajes,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            curp=curp,
            email=email,
            enviar_boletin=enviar_boletin,
            estatus=estatus,
            nombres=nombres,
            settings=settings,
            telefono=telefono,
            tiene_contrasena_sha256=tiene_contrasena_sha256,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_clientes.get("/creados_por_dia", response_model=CustomList[CitClienteCreadosPorDiaOut])
async def cantidades_clientes_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    size: int = 100,
):
    """Calcular cantidades de clientes creados por dia"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes_creados_por_dia(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            settings=settings,
            size=size,
        )
    except CitasAnyError as error:
        return custom_list_success_false(error)
    items = [CitClienteCreadosPorDiaOut(creado=creado, cantidad=cantidad) for creado, cantidad in resultados.all()]
    total = sum(item.cantidad for item in items)
    result = ListResult(total=total, items=items, size=size)
    return CustomList(result=result)


@cit_clientes.get("/perfil", response_model=OneCitClienteOut)
async def perfil_cliente(
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Consultar el perfil de un cliente por su ID, CURP o email"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente = get_cit_cliente(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
        )
    except CitasAnyError as error:
        return OneCitClienteOut(success=False, message=str(error))
    return OneCitClienteOut.from_orm(cit_cliente)


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
