"""
Cit Citas v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from config.settings import LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave, safe_email, safe_string

from .models import CitCita
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente
from ..cit_servicios.crud import get_cit_servicio
from ..cit_servicios.models import CitServicio
from ..oficinas.crud import get_oficina
from ..oficinas.models import Oficina

DEFAULT_DIAS = 7


def get_cit_citas(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha: date = None,
    estado: str = None,
    inicio_desde: datetime = None,
    inicio_hasta: datetime = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(CitCita.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=True)
        if cit_cliente_email is None or cit_cliente_email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitCita.cit_servicio == cit_servicio)
    if creado:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCita.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCita.creado <= hasta_dt)
    if fecha is not None:
        inicio_desde = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
        inicio_hasta = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)
        consulta = consulta.filter(CitCita.inicio >= inicio_desde)
        consulta = consulta.filter(CitCita.inicio <= inicio_hasta)
    else:
        if inicio_desde is not None:
            consulta = consulta.filter(CitCita.inicio >= inicio_desde)
        if inicio_hasta is not None:
            consulta = consulta.filter(CitCita.inicio <= inicio_hasta)
    if estado is None:
        consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))  # Si no se especifica, se filtra
    else:
        estado = safe_string(estado)
        if estado not in CitCita.ESTADOS:
            raise CitasNotValidParamError("El estado no es válido")
        consulta = consulta.filter(CitCita.estado == estado)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitCita.oficina == oficina)
    elif oficina_clave is not None:
        oficina_clave = safe_clave(oficina_clave)
        if oficina_clave is None or oficina_clave == "":
            raise CitasNotValidParamError("No es válida la clave de la oficina")
        consulta = consulta.join(Oficina)
        consulta = consulta.filter(Oficina.clave == oficina_clave)
    consulta = consulta.filter_by(estatus="A")
    if fecha is not None:
        consulta = consulta.order_by(CitCita.inicio)
    else:
        consulta = consulta.order_by(CitCita.id.desc())
    return consulta


def get_cit_cita(db: Session, cit_cita_id: int) -> CitCita:
    """Consultar un cita por su id"""
    cit_cita = db.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise CitasNotExistsError("No existe ese cita")
    if cit_cita.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cita, está eliminado")
    return cit_cita


def get_cit_citas_creados_por_dia(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Calcular las cantidades de citas creados por dia"""

    # Observe que para la columna `creado` se usa la función func.date()
    consulta = db.query(
        func.date(CitCita.creado).label("creado"),
        func.count(CitCita.id).label("cantidad"),
    )

    # Filtrar estados
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))

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
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCita.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por la fecha de creacion y entregar SIN hacer la consulta
    return consulta.group_by(func.date(CitCita.creado)).order_by(func.date(CitCita.creado))


def get_cit_citas_agendadas_por_servicio_oficina(
    db: Session,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
) -> Any:
    """Calcular las cantidades de citas agendadas por servicio y oficina"""

    # Consultar las columnas oficina clave, servicio clave y cantidad
    consulta = db.query(
        Oficina.clave.label("oficina"),
        CitServicio.clave.label("servicio"),
        func.count("*").label("cantidad"),
    )

    # Juntar las tablas de oficina y servicio
    consulta = consulta.select_from(CitCita).join(CitServicio, Oficina)

    # Filtrar estatus
    consulta = consulta.filter(CitCita.estatus == "A")
    consulta = consulta.filter(CitServicio.estatus == "A")
    consulta = consulta.filter(Oficina.estatus == "A")

    # Filtrar estados
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))

    # Si NO se reciben inicios, se limitan a los últimos DEFAULT_DIAS días
    if inicio is None and inicio_desde is None and inicio_hasta is None:
        hoy_servidor = datetime.now(SERVIDOR_HUSO_HORARIO)
        hoy = hoy_servidor.astimezone(LOCAL_HUSO_HORARIO).date()
        inicio_desde = hoy - timedelta(days=DEFAULT_DIAS)
        inicio_hasta = hoy

    # Si se recibe inicio, se limita a esa fecha
    if inicio:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    else:
        if inicio_desde:
            desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta:
            hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por oficina y servicio y entregar SIN hacer la consulta
    return consulta.group_by(Oficina.clave, CitServicio.clave).order_by(Oficina.clave, CitServicio.clave)
