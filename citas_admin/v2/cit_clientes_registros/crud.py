"""
Cit Clientes Registros v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from config.settings import LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string

from .models import CitClienteRegistro

DEFAULT_DIAS = 7


def get_cit_clientes_registros(
    db: Session,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    ya_registrado: bool = None,
) -> Any:
    """Consultar los registros de clientes activos"""
    consulta = db.query(CitClienteRegistro)
    apellido_primero = safe_string(apellido_primero)
    if apellido_primero is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_primero.contains(apellido_primero))
    apellido_segundo = safe_string(apellido_segundo)
    if apellido_segundo is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_segundo.contains(apellido_segundo))
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)
    curp = safe_curp(curp, search_fragment=True)
    if curp is not None:
        consulta = consulta.filter(CitClienteRegistro.curp.contains(curp))
    if email is not None:
        email = safe_email(email, search_fragment=True)
        if email is None or email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.filter(CitClienteRegistro.email.contains(email))
    nombres = safe_string(nombres)
    if nombres is not None:
        consulta = consulta.filter(CitClienteRegistro.nombres.contains(nombres))
    if ya_registrado is None:
        consulta = consulta.filter_by(ya_registrado=False)  # Si no se especifica, se filtra por no registrados
    else:
        consulta = consulta.filter_by(ya_registrado=ya_registrado)
    return consulta.filter_by(estatus="A").order_by(CitClienteRegistro.id.desc())


def get_cit_cliente_registro(db: Session, cit_cliente_registro_id: int) -> CitClienteRegistro:
    """Consultar un registro de cliente por su id"""
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise CitasNotExistsError("No existe ese registro de cliente")
    if cit_cliente_registro.estatus != "A":
        raise CitasIsDeletedError("No es activo ese registro de cliente, está eliminado")
    return cit_cliente_registro


def get_cit_clientes_registros_creados_por_dia(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Calcular las cantidades de registros de clientes creados por dia"""
    # Observe que para la columna `creado` se usa la función func.date()
    consulta = db.query(
        func.date(CitClienteRegistro.creado).label("creado"),
        func.count(CitClienteRegistro.id).label("cantidad"),
    )
    # Si NO se reciben creados, se limitan a los últimos DEFAULT_DIAS días
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy_servidor = datetime.now(SERVIDOR_HUSO_HORARIO)
        hoy = hoy_servidor.astimezone(LOCAL_HUSO_HORARIO).date()
        creado_desde = hoy - timedelta(days=DEFAULT_DIAS)
        creado_hasta = hoy
    # Si se recibe creado, se limita a esa fecha
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)
    return consulta.group_by(func.date(CitClienteRegistro.creado))
