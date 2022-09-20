"""
Cit Citas v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, make_custom_error_page
from lib.fastapi_pagination_custom_list import CustomList, ListResult, make_custom_error_list

from .crud import create_cit_cita, get_cit_citas, get_cit_cita, get_cit_citas_creados_por_dia, get_cit_citas_agendadas_por_servicio_oficina, get_mis_citas
from .schemas import CitCitaIn, CitCitaOut, CitCitasCreadosPorDiaOut, CitCitasAgendadasPorServicioOficinaOut, OneCitCitaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_citas = APIRouter(prefix="/v2/cit_citas", tags=["citas citas"])


@cit_citas.get("", response_model=CustomPage[CitCitaOut])
async def listado_citas(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Listado de citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            cit_servicio_id=cit_servicio_id,
            cit_servicio_clave=cit_servicio_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            estado=estado,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            settings=settings,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@cit_citas.get("/creados_por_dia", response_model=CustomList[CitCitasCreadosPorDiaOut])
async def cantidades_creados_por_dia(
    db: Session = Depends(get_db),
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    distrito_id: int = None,
    settings: Settings = Depends(get_settings),
    size: int = 10,
):
    """Calcular las cantidades de citas creadas por dia"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas_creados_por_dia(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            settings=settings,
            size=size,
        )
    except CitasAnyError as error:
        return make_custom_error_list(error)
    items = [CitCitasCreadosPorDiaOut(creado=creado, cantidad=cantidad) for creado, cantidad in resultados.all()]
    result = ListResult(total=resultados.count(), items=items, size=size)
    return CustomList(result=result)


@cit_citas.get("/agendadas_por_servicio_oficina", response_model=CustomList[CitCitasAgendadasPorServicioOficinaOut])
async def cantidades_citas_agendadas_por_servicio_oficina(
    db: Session = Depends(get_db),
    current_user: UsuarioInDB = Depends(get_current_active_user),
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    settings: Settings = Depends(get_settings),
    size: int = 10,
):
    """Calcular las cantidades de citas agendadas por oficina y servicio"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas_agendadas_por_servicio_oficina(
            db=db,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            settings=settings,
            size=size,
        )
    except CitasAnyError as error:
        return make_custom_error_list(error)
    items = [CitCitasAgendadasPorServicioOficinaOut(oficina=oficina, servicio=servicio, cantidad=cantidad) for oficina, servicio, cantidad in resultados.all()]
    result = ListResult(total=resultados.count(), items=items, size=size)
    return CustomList(result=result)


@cit_citas.post("/nueva", response_model=OneCitCitaOut)
async def nueva_cita(
    datos: CitCitaIn,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Crear una nueva cita"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = create_cit_cita(
            db=db,
            cit_cliente_id=datos.cit_cliente_id,
            cit_servicio_id=datos.cit_servicio_id,
            fecha=datos.fecha,
            hora_minuto=datos.hora_minuto,
            oficina_id=datos.oficina_id,
            notas=datos.notas,
            settings=settings,
        )
    except CitasAnyError as error:
        return OneCitCitaOut(success=False, message=str(error))
    return OneCitCitaOut.from_orm(cit_cita)


@cit_citas.get("/mis_citas", response_model=CustomPage[CitCitaOut])
async def mis_citas(
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Mis citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_mis_citas(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
            settings=settings,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@cit_citas.get("/{cit_cita_id}", response_model=OneCitCitaOut)
async def detalle_cita(
    cit_cita_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una citas a partir de su id"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = get_cit_cita(
            db=db,
            cit_cita_id=cit_cita_id,
        )
    except CitasAnyError as error:
        return OneCitCitaOut(success=False, message=str(error))
    return OneCitCitaOut.from_orm(cit_cita)
