"""
Oficinas v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_oficinas, get_oficina
from .schemas import OficinaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

oficinas = APIRouter(prefix="/v2/oficinas", tags=["catalogos"])


@oficinas.get("", response_model=LimitOffsetPage[OficinaOut])
async def listado_oficinas(
    distrito_id: int = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    puede_agendar_citas: bool = None,
    puede_enviar_qr: bool = False,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_oficinas(
            db,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            es_jurisdiccional=es_jurisdiccional,
            puede_agendar_citas=puede_agendar_citas,
            puede_enviar_qr=puede_enviar_qr,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@oficinas.get("/{oficina_id}", response_model=OficinaOut)
async def detalle_oficina(
    oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficinas a partir de su id"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina(
            db,
            oficina_id=oficina_id,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return OficinaOut.from_orm(oficina)
