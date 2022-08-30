"""
Cit Citas v2, rutas (paths)
"""
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_cit_citas, get_cit_cita, get_cit_citas_creados_por_dia, get_cit_citas_agendadas_por_servicio_oficina
from .schemas import CitCitaOut, CitCitasCreadosPorDiaOut, CitCitasAgendadasPorServicioOficinaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_citas = APIRouter(prefix="/v2/cit_citas", tags=["citas citas"])


@cit_citas.get("", response_model=LimitOffsetPage[CitCitaOut])
async def listado_citas(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    inicio: date = None,
    inicio_desde: datetime = None,
    inicio_hasta: datetime = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultado = get_cit_citas(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            cit_servicio_id=cit_servicio_id,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            estado=estado,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(resultado)


@cit_citas.get("/creados_por_dia", response_model=CitCitasCreadosPorDiaOut)
async def cantidades_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Calcular las cantidades de citas creadas por dia"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        fechas_cantidades = get_cit_citas_creados_por_dia(
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
    return CitCitasCreadosPorDiaOut(items=fechas_cantidades, total=total)


@cit_citas.get("/agendadas_por_servicio_oficina", response_model=CitCitasAgendadasPorServicioOficinaOut)
async def cantidades_citas_agendadas_por_servicio_oficina(
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Calcular las cantidades de citas agendadas por oficina y servicio"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficinas_servicios_cantidades = get_cit_citas_agendadas_por_servicio_oficina(
            db=db,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
        ).all()  # Observe que se ejecuta la consulta
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    total = 0
    for oficina_servicio_cantidad in oficinas_servicios_cantidades:
        total += oficina_servicio_cantidad["cantidad"]
    return CitCitasAgendadasPorServicioOficinaOut(items=oficinas_servicios_cantidades, total=total)


@cit_citas.get("/{cit_cita_id}", response_model=CitCitaOut)
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
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitCitaOut.from_orm(cit_cita)
