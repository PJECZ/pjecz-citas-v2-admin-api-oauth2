"""
FastAPI Pagination Custom
"""
from typing import Generic, List, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.limit_offset import LimitOffsetParams as BaseLimitOffsetParams
from pydantic.generics import GenericModel

T = TypeVar("T")


class LimitOffsetParams(BaseLimitOffsetParams):
    """Agregar los parametros de paginacion limit y offset"""

    limit: int = Query(100, ge=1, le=1000, description="Query limit")
    offset: int = Query(1, ge=1, description="Query offset")


class PageResult(GenericModel, Generic[T]):
    """Resultado para la paginacion que contiene items, total, limit y offset"""

    total: int
    items: List[T]
    limit: int
    offset: int


class CustomPage(AbstractPage[T], Generic[T]):
    """Pagina personalizada"""

    success: bool = True
    message: str = "Success"
    result: PageResult[T]

    __params_type__ = LimitOffsetParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams):
        """Create"""

        if not isinstance(params, cls.__params_type__):
            raise TypeError(f"Params must be {cls.__params_type__}")

        return cls(
            result=PageResult(
                total=total,
                items=items,
                limit=params.limit,
                offset=params.offset,
            )
        )


def make_custom_error_page(error: Exception) -> CustomPage:
    """Crear pagina de error"""

    result = PageResult(total=0, items=[], limit=0, offset=0)
    return CustomPage(success=False, message=str(error), result=result)
