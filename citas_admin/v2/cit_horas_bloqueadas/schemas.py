"""
Cit Horas Bloqueadas v2, esquemas de pydantic
"""
from datetime import date, time
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitHoraBloqueadaOut(BaseModel):
    """Esquema para entregar horas bloqueadas"""

    id: int | None
    oficina_id: int | None
    oficina_clave: str | None
    oficina_descripcion: str | None
    oficina_descripcion_corta: str | None
    fecha: date | None
    inicio: time | None
    termino: time | None
    descripcion: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitHoraBloqueadaOut(CitHoraBloqueadaOut, OneBaseOut):
    """Esquema para entregar una hora bloqueada"""
