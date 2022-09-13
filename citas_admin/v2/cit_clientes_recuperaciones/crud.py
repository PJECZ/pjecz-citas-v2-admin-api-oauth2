"""
Cit Clientes Recuperaciones v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import pytz

from config.settings import Settings
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_email

from .models import CitClienteRecuperacion
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente

DEFAULT_DIAS = 7


def get_cit_clientes_recuperaciones(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
) -> Any:
    """Consultar las recuperaciones"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(CitClienteRecuperacion)
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, get_cit_cliente)
        consulta = consulta.filter(CitClienteRecuperacion.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=True)
        if cit_cliente_email is None or cit_cliente_email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCliente.creado >= desde_dt).filter(CitCliente.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitCliente.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitCliente.creado <= hasta_dt)
    if ya_recuperado is None:
        consulta = consulta.filter_by(ya_recuperado=False)  # Si no se especifica, se filtra por no recuperados
    else:
        consulta = consulta.filter_by(ya_recuperado=ya_recuperado)
    return consulta.filter_by(estatus="A").order_by(CitClienteRecuperacion.id.desc())


def get_cit_cliente_recuperacion(db: Session, cit_cliente_recuperacion_id: int) -> CitClienteRecuperacion:
    """Consultar una recuperacion por su id"""
    cit_cliente_recuperacion = db.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if cit_cliente_recuperacion is None:
        raise CitasNotExistsError("No existe ese recuperacion")
    if cit_cliente_recuperacion.estatus != "A":
        raise CitasIsDeletedError("No es activo ese recuperacion, está eliminado")
    return cit_cliente_recuperacion


def get_cit_clientes_recuperaciones_creados_por_dia(
    db: Session,
    settings: Settings,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Calcular las cantidades de recuperaciones de clientes creados por dia"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Observe que para la columna `creado` se usa la función func.date()
    consulta = db.query(
        func.date(CitClienteRecuperacion.creado).label("creado"),
        func.count(CitClienteRecuperacion.id).label("cantidad"),
    )

    # Si NO se reciben creados, se limitan a los últimos DEFAULT_DIAS días
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy_servidor = datetime.now(servidor_huso_horario)
        hoy = hoy_servidor.astimezone(local_huso_horario).date()
        creado_desde = hoy - timedelta(days=DEFAULT_DIAS)
        creado_hasta = hoy

    # Si se recibe creado, se limita a esa fecha
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRecuperacion.creado >= desde_dt).filter(CitClienteRecuperacion.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitClienteRecuperacion.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitClienteRecuperacion.creado <= hasta_dt)

    # Agrupar por creado y entregar SIN hacer la consulta
    return consulta.group_by(func.date(CitClienteRecuperacion.creado))
