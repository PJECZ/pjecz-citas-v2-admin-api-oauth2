"""
Pagos Pagos v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_pag_pagos, get_pag_pago
from .schemas import PagPagoOut, OnePagPagoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

pag_pagos = APIRouter(prefix="/v2/pag_pagos", tags=["pagos"])


@pag_pagos.get("", response_model=CustomPage[PagPagoOut])
async def listado_pag_pagos(
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    pag_tramite_servicio_id: int = None,
    estado: str = None,
    estatus: str = None,
    ya_se_envio_comprobante: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de pagos"""
    if current_user.permissions.get("PAG PAGOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_pag_pagos(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
            pag_tramite_servicio_id=pag_tramite_servicio_id,
            estado=estado,
            estatus=estatus,
            ya_se_envio_comprobante=ya_se_envio_comprobante,
        )
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@pag_pagos.get("/{pag_pago_id}", response_model=OnePagPagoOut)
async def detalle_pag_pago(
    pag_pago_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una pagos a partir de su id"""
    if current_user.permissions.get("PAG PAGOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        pag_pago = get_pag_pago(
            db=db,
            pag_pago_id=pag_pago_id,
        )
    except CitasAnyError as error:
        return OnePagPagoOut(success=False, message=str(error))
    return OnePagPagoOut.from_orm(pag_pago)
