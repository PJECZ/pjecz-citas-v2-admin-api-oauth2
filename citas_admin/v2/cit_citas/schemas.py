"""
Cit Citas v2, esquemas de pydantic
"""
from datetime import datetime
from pydantic import BaseModel


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    cit_servicio_id: int
    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime
    notas: str
    estado: str
    asistencia: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
