"""
Encuestas Servicios v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_enc_servicios, get_enc_servicio
from .schemas import EncServicioOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

enc_servicios = APIRouter(prefix="/v2/enc_servicios", tags=["encuestas"])


@enc_servicios.get("", response_model=LimitOffsetPage[EncServicioOut])
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
):
    """Listado de encuestas de servicios"""
    if current_user.permissions.get("ENC SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_enc_servicios(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estado=estado,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except (CitasIsDeletedError, CitasNotExistsError) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@enc_servicios.get("/{enc_servicio_id}", response_model=EncServicioOut)
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
    except (CitasIsDeletedError, CitasNotExistsError) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncServicioOut.from_orm(enc_servicio)
