"""
Cit Clientes Registros v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import pytz

from config.settings import Settings
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string

from .models import CitClienteRegistro


def get_cit_clientes_registros(
    db: Session,
    settings: Settings,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    estatus: str = None,
    nombres: str = None,
    ya_registrado: bool = None,
) -> Any:
    """Consultar los registros de clientes activos"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(CitClienteRegistro)

    # Filtrar por apellido primero
    apellido_primero = safe_string(apellido_primero)
    if apellido_primero is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_primero.contains(apellido_primero))

    # Filtrar por apedillo segundo
    apellido_segundo = safe_string(apellido_segundo)
    if apellido_segundo is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_segundo.contains(apellido_segundo))

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por fragmento de CURP
    curp = safe_curp(curp, search_fragment=True)
    if curp is not None:
        consulta = consulta.filter(CitClienteRegistro.curp.contains(curp))

    # Filtrar por fragmento de email
    if email is not None:
        email = safe_email(email, search_fragment=True)
        if email is None or email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.filter(CitClienteRegistro.email.contains(email))

    # Filtrar por nombres
    nombres = safe_string(nombres)
    if nombres is not None:
        consulta = consulta.filter(CitClienteRegistro.nombres.contains(nombres))

    # Filtrar por ya registrado
    if ya_registrado is None:
        consulta = consulta.filter_by(ya_registrado=False)  # Si no se especifica, se filtra por no registrados
    else:
        consulta = consulta.filter_by(ya_registrado=ya_registrado)

    # Entregar
    return consulta.order_by(CitClienteRegistro.id.desc())


def get_cit_cliente_registro(
    db: Session,
    cit_cliente_registro_id: int,
) -> CitClienteRegistro:
    """Consultar un registro de cliente por su id"""
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise CitasNotExistsError("No existe ese registro de cliente")
    if cit_cliente_registro.estatus != "A":
        raise CitasIsDeletedError("No es activo ese registro de cliente, está eliminado")
    return cit_cliente_registro


def get_cit_clientes_registros_creados_por_dia(
    db: Session,
    settings: Settings,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Calcular las cantidades de registros de clientes creados por dia"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Observe que para la columna `creado` se usa la función func.date()
    consulta = db.query(
        func.date(CitClienteRegistro.creado).label("creado"),
        func.count(CitClienteRegistro.id).label("cantidad"),
    )

    # Si NO se reciben creados, se limitan a los últimos DEFAULT_DIAS días
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy_servidor = datetime.now(servidor_huso_horario)
        hoy = hoy_servidor.astimezone(local_huso_horario).date()
        creado_desde = hoy - timedelta(days=size - 1)
        creado_hasta = hoy

    # Si se recibe creado, se limita a esa fecha
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)

    # Agrupar por creado y entregar
    return consulta.group_by(func.date(CitClienteRegistro.creado))
