"""
Encuestas Sistemas v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, make_custom_error_page

from .crud import get_enc_sistemas, get_enc_sistema, get_enc_sistema_url
from .schemas import EncSistemaOut, OneEncSistemaOut, OneEncSistemaURLOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

enc_sistemas = APIRouter(prefix="/v2/enc_sistemas", tags=["encuestas"])


@enc_sistemas.get("", response_model=CustomPage[EncSistemaOut])
async def listado_encuestas_sistemas(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Listado de encuestas de sistemas"""
    if current_user.permissions.get("ENC SISTEMAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_enc_sistemas(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estado=estado,
            settings=settings,
        )
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@enc_sistemas.get("/pendiente", response_model=OneEncSistemaURLOut)
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
        url = get_enc_sistema_url(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
            settings=settings,
        )
    except CitasAnyError as error:
        return OneEncSistemaURLOut(success=False, message=str(error))
    return OneEncSistemaURLOut(success=True, url=url)


@enc_sistemas.get("/{enc_sistema_id}", response_model=OneEncSistemaOut)
async def detalle_encuestas_sistema(
    enc_sistema_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una encuestas de sistemas a partir de su id"""
    if current_user.permissions.get("ENC SISTEMAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        enc_sistema = get_enc_sistema(db, enc_sistema_id=enc_sistema_id)
    except CitasAnyError as error:
        return OneEncSistemaOut(success=False, message=str(error))
    return OneEncSistemaOut.from_orm(enc_sistema)
