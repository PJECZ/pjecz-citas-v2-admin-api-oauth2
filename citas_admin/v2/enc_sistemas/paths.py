"""
Encuestas Sistemas v2, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_enc_sistemas, get_enc_sistema
from .schemas import EncSistemaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

enc_sistemas = APIRouter(prefix="/v2/enc_sistemas", tags=["encuestas"])


@enc_sistemas.get("", response_model=LimitOffsetPage[EncSistemaOut])
async def listado_encuestas_sistemas(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de encuestas de sistemas"""
    if current_user.permissions.get("ENC SISTEMAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_enc_sistemas(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estado=estado,
        )
    except (CitasIsDeletedError, CitasNotExistsError) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@enc_sistemas.get("/{enc_sistema_id}", response_model=EncSistemaOut)
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
    except (CitasIsDeletedError, CitasNotExistsError) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncSistemaOut.from_orm(enc_sistema)
