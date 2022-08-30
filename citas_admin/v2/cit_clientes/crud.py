"""
Cit Clientes v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from config.settings import LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string

from .models import CitCliente

DEFAULT_DIAS = 7


def get_cit_clientes(
    db: Session,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    enviar_boletin: bool = None,
    nombres: str = None,
    tiene_contrasena_sha256: bool = None,
) -> Any:
    """Consultar los clientes activos"""
    consulta = db.query(CitCliente)
    apellido_primero = safe_string(apellido_primero)
    if apellido_primero is not None:
        consulta = consulta.filter(CitCliente.apellido_primero.contains(apellido_primero))
    apellido_segundo = safe_string(apellido_segundo)
    if apellido_segundo is not None:
        consulta = consulta.filter(CitCliente.apellido_segundo.contains(apellido_segundo))
    curp = safe_curp(curp, search_fragment=True)
    if creado:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(CitCliente.creado >= desde_dt).filter(CitCliente.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCliente.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCliente.creado <= hasta_dt)
    if curp is not None:
        consulta = consulta.filter(CitCliente.curp.contains(curp))
    if email is not None:
        email = safe_email(email, search_fragment=True)
        if email is None or email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.filter(CitCliente.email.contains(email))
    if enviar_boletin is not None:
        consulta = consulta.filter(CitCliente.enviar_boletin == enviar_boletin)
    nombres = safe_string(nombres)
    if nombres is not None:
        consulta = consulta.filter(CitCliente.nombres.contains(nombres))
    if tiene_contrasena_sha256 is not None:
        if tiene_contrasena_sha256:
            consulta = consulta.filter(CitCliente.contrasena_sha256 != "")
        else:
            consulta = consulta.filter(CitCliente.contrasena_sha256 == "")
    return consulta.filter_by(estatus="A").order_by(CitCliente.id.desc())


def get_cit_cliente(db: Session, cit_cliente_id: int) -> CitCliente:
    """Consultar un cliente por su id"""
    cit_cliente = db.query(CitCliente).get(cit_cliente_id)
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_clientes_cantidades_creados_por_dia(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Calcular las cantidades de clientes creados por dia"""
    # Observe que para la columna creado se usa la función func.date()
    consulta = db.query(
        func.date(CitCliente.creado).label("creado"),
        func.count(CitCliente.id).label("cantidad"),
    )
    # Si NO se reciben creados, se limitan a los últimos DEFAULT_DIAS días
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy_servidor = datetime.now(SERVIDOR_HUSO_HORARIO)
        hoy = hoy_servidor.astimezone(LOCAL_HUSO_HORARIO).date()
        creado_desde = hoy - timedelta(days=DEFAULT_DIAS)
        creado_hasta = hoy
    # Si se recibe creado, se limita a esa fecha
    if creado:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(CitCliente.creado >= desde_dt).filter(CitCliente.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCliente.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCliente.creado <= hasta_dt)
    return consulta.group_by(func.date(CitCliente.creado))
