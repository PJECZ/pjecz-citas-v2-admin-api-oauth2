"""
Cit Categorias v2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, make_custom_error_page

from .crud import get_cit_categorias, get_cit_categoria
from .schemas import CitCategoriaOut, OneCitCategoriaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

cit_categorias = APIRouter(prefix="/v2/cit_categorias", tags=["citas categorias"])


@cit_categorias.get("", response_model=CustomPage[CitCategoriaOut])
async def listado_categorias(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de categorias"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_categorias(db=db)
    except CitasAnyError as error:
        return make_custom_error_page(error)
    return paginate(resultados)


@cit_categorias.get("/{cit_categoria_id}", response_model=OneCitCategoriaOut)
async def detalle_categoria(
    cit_categoria_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una categorias a partir de su id"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_categoria = get_cit_categoria(
            db=db,
            cit_categoria_id=cit_categoria_id,
        )
    except CitasAnyError as error:
        return OneCitCategoriaOut(success=False, message=str(error))
    return OneCitCategoriaOut.from_orm(cit_categoria)
