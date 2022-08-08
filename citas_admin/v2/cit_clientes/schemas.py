"""
Cit Clientes v2, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    id: int
    nombres: str
    apellido_primero: str
    apellido_segundo: str
    curp: str
    telefono: str
    email: str
    contrasena_md5: str
    contrasena_sha256: str
    renovacion: date
    nombre: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
