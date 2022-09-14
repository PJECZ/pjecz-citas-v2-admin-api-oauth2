"""
Cit Dias Disponibles v2, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitDiaDisponibleOut(BaseModel):
    """Esquema para entregar dia disponible"""

    fecha: date
