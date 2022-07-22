"""
Cit Horas Bloqueadas v2, esquemas de pydantic
"""
from datetime import date, time
from pydantic import BaseModel


class CitHoraBloqueadaOut(BaseModel):
    """Esquema para entregar horas bloqueadas"""

    id: int
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    fecha: date
    inicio: time
    termino: time
    descripcion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
