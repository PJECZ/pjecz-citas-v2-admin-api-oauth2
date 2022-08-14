"""
Cit Dias Disponibles v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
import pytz

from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles

LIMITE_DIAS = 90
QUITAR_PRIMER_DIA_DESPUES_HORAS = 14
SERVIDOR_HUSO_HORARIO = pytz.utc
LOCAL_HUSO_HORARIO = pytz.timezone("America/Mexico_City")


def get_cit_dias_disponibles(
    db: Session,
    limit: int = LIMITE_DIAS,
) -> Any:
    """Consultar los dias disponibles, entrega un listado de fechas"""
    dias_disponibles = []

    # Consultar dias inhabiles
    fechas_inhabiles = []
    cit_dias_inhabiles = get_cit_dias_inhabiles(db).all()
    if len(cit_dias_inhabiles) > 0:
        fechas_inhabiles = [item.fecha for item in cit_dias_inhabiles]

    # Agregar cada dia hasta el limite a partir de manana
    for fecha in (date.today() + timedelta(n) for n in range(1, LIMITE_DIAS)):

        # Quitar los sabados y domingos
        if fecha.weekday() in (5, 6):
            continue

        # Quitar los dias inhabiles
        if fecha in fechas_inhabiles:
            continue

        # Acumular
        dias_disponibles.append(fecha)

    # Definir tiempo local
    servidor_tiempo = datetime.now(SERVIDOR_HUSO_HORARIO)
    tiempo_local = servidor_tiempo.astimezone(LOCAL_HUSO_HORARIO)

    # Definir que dia es hoy
    hoy = tiempo_local.date()

    # Definir si hoy es sabado, domingo o dia inhabil
    hoy_es_dia_inhabil = hoy.weekday() in (5, 6) or hoy in fechas_inhabiles

    # Si hoy es dia inhabil, quitar el primer dia disponible
    if hoy_es_dia_inhabil:
        dias_disponibles.pop(0)

    # Si es dia habil y pasan de las QUITAR_PRIMER_DIA_DESPUES_HORAS horas, quitar el primer dia disponible
    elif tiempo_local.hour >= QUITAR_PRIMER_DIA_DESPUES_HORAS:
        dias_disponibles.pop(0)

    # Elaborar respuesta como listado de dicionarios
    respuesta = []
    for fecha in dias_disponibles:
        respuesta.append({"fecha": fecha})
        if len(respuesta) >= limit:
            break

    # Entregar
    return respuesta


def get_cit_dia_disponible(db: Session) -> Any:
    """Obtener el proximo dia disponible, por ejemplo, si hoy es viernes y el lunes es dia inhabil, entrega el martes"""

    # Consultar dias inhabiles
    fechas_inhabiles = []
    cit_dias_inhabiles = get_cit_dias_inhabiles(db).all()
    if len(cit_dias_inhabiles) > 0:
        fechas_inhabiles = [item.fecha for item in cit_dias_inhabiles]

    # Determinar la fecha, primero se usa el dia de mañana
    fecha = date.today() + timedelta(1)

    # Bucle para saltar al siguiente dia si es sabado, domingo o dia inhabil
    while fecha.weekday() in (5, 6) or fecha in fechas_inhabiles:
        fecha = fecha + timedelta(1)

    # Entregar
    return {"fecha": fecha}
