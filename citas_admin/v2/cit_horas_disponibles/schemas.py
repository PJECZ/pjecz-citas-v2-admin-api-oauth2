"""
Cit Horas Disponibles V2, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel


class CitHoraDisponibleOut(BaseModel):
    """Esquema para entregar hora disponible"""

    horas_minutos: time
