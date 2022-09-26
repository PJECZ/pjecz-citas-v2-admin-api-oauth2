"""
Encuestas Servicios v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_enc_servicios, get_enc_servicio, get_enc_servicio_url
from .schemas import EncServicioOut, OneEncServicioOut, OneEncServicioURLOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

enc_servicios = APIRouter(prefix="/v2/enc_servicios", tags=["encuestas"])


@enc_servicios.get("", response_model=CustomPage[EncServicioOut])
async def listado_encuestas_servicios(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Listado de encuestas de servicios"""
    if current_user.permissions.get("ENC SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_enc_servicios(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estado=estado,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            settings=settings,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@enc_servicios.get("/pendiente", response_model=OneEncServicioURLOut)
async def pendiente_encuesta_servicio(
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Entrega la URL de la encuesta de servicio PENDIENTE si existe"""
    if current_user.permissions.get("ENC SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        url = get_enc_servicio_url(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
            settings=settings,
        )
    except CitasAnyError as error:
        return OneEncServicioURLOut(success=False, message=str(error))
    return OneEncServicioURLOut(success=True, url=url)


@enc_servicios.get("/{enc_servicio_id}", response_model=OneEncServicioOut)
async def detalle_encuestas_servicio(
    enc_servicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una encuestas de servicios a partir de su id"""
    if current_user.permissions.get("ENC SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        enc_servicio = get_enc_servicio(db, enc_servicio_id=enc_servicio_id)
    except CitasAnyError as error:
        return OneEncServicioOut(success=False, message=str(error))
    return OneEncServicioOut.from_orm(enc_servicio)
