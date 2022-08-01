"""
Cit Citas v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException
from lib.safe_string import safe_clave, safe_email

from .models import CitCita
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina
from ..oficinas.models import Oficina

HOY = date.today()
ANTIGUA_FECHA = date(year=2022, month=1, day=1)


def get_cit_citas(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    inicio_desde: datetime = None,
    inicio_hasta: datetime = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(CitCita.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=True)
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitCita.cit_servicio == cit_servicio)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitCita.oficina == oficina)
    elif oficina_clave is not None:
        oficina_clave = safe_clave(oficina_clave)
        consulta = consulta.join(Oficina)
        consulta = consulta.filter(Oficina.clave == oficina_clave)
    if inicio_desde is not None:
        consulta = consulta.filter(CitCita.inicio >= inicio_desde)
    if inicio_hasta is not None:
        consulta = consulta.filter(CitCita.inicio <= inicio_hasta)
    if creado_desde is not None:
        if not ANTIGUA_FECHA <= creado_desde <= HOY:
            raise OutOfRangeException("Creado desde fuera de rango")
        consulta = consulta.filter(func.date(CitCita.creado) >= creado_desde)
    if creado_hasta is not None:
        if not ANTIGUA_FECHA <= creado_hasta <= HOY:
            raise OutOfRangeException("Creado hasta fuera de rango")
        consulta = consulta.filter(func.date(CitCita.creado) <= creado_hasta)
    return consulta.filter_by(estatus="A").order_by(CitCita.id.desc())


def get_cit_cita(db: Session, cit_cita_id: int) -> CitCita:
    """Consultar un cita por su id"""
    cit_cita = db.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise NotExistsException("No existe ese cita")
    if cit_cita.estatus != "A":
        raise IsDeletedException("No es activo ese cita, está eliminado")
    return cit_cita


def get_cit_citas_cantidades_creados_por_dia(
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
    # Si se recibe creado, se limita a esa fecha
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise OutOfRangeException("Creado fuera de rango")
        consulta = consulta.filter(func.date(CitCita.creado) == creado)
    else:
        # Si se reciben creado_desde y creado_hasta, validar que sean correctos
        if creado_desde and creado_hasta:
            if creado_desde > creado_hasta:
                raise OutOfRangeException("El rango de fechas no es correcto")
        # Si NO se reciben creado_desde y creado_hasta, se limitan a los últimos 30 días
        if creado_desde is None and creado_hasta is None:
            creado_desde = HOY - timedelta(days=30)
            creado_hasta = HOY
        # Si solo se recibe creado_desde, entonces creado_hasta es HOY
        if creado_desde and creado_hasta is None:
            creado_hasta = HOY
        if creado_desde is not None:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise OutOfRangeException("Creado desde fuera de rango")
            consulta = consulta.filter(func.date(CitCita.creado) >= creado_desde)
        if creado_hasta is not None:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise OutOfRangeException("Creado hasta fuera de rango")
            consulta = consulta.filter(func.date(CitCita.creado) <= creado_hasta)
    return consulta.group_by(func.date(CitCita.creado))
