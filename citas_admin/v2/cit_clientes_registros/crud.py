"""
Cit Clientes Registros v2, CRUD (create, read, update, and delete)
"""
from datetime import date, timedelta
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasOutOfRangeParamError
from lib.safe_string import safe_curp, safe_email, safe_string

from .models import CitClienteRegistro

HOY = date.today()
ANTIGUA_FECHA = date(year=2022, month=1, day=1)


def get_cit_clientes_registros(
    db: Session,
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    ya_registrado: bool = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Consultar los registros de clientes activos"""
    consulta = db.query(CitClienteRegistro)
    nombres = safe_string(nombres)
    if nombres is not None:
        consulta = consulta.filter(CitClienteRegistro.nombres.contains(nombres))
    apellido_primero = safe_string(apellido_primero)
    if apellido_primero is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_primero.contains(apellido_primero))
    apellido_segundo = safe_string(apellido_segundo)
    if apellido_segundo is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_segundo.contains(apellido_segundo))
    curp = safe_curp(curp, search_fragment=True)
    if curp is not None:
        consulta = consulta.filter(CitClienteRegistro.curp.contains(curp))
    email = safe_email(email, search_fragment=True)
    if email is not None:
        consulta = consulta.filter(CitClienteRegistro.email.contains(email))
    if ya_registrado is not None:
        consulta = consulta.filter_by(ya_registrado=ya_registrado)
    if creado_desde is not None:
        if not ANTIGUA_FECHA <= creado_desde <= HOY:
            raise CitasOutOfRangeParamError("Creado desde fuera de rango")
        consulta = consulta.filter(func.date(CitClienteRegistro.creado) >= creado_desde)
    if creado_hasta is not None:
        if not ANTIGUA_FECHA <= creado_hasta <= HOY:
            raise CitasOutOfRangeParamError("Creado hasta fuera de rango")
        consulta = consulta.filter(func.date(CitClienteRegistro.creado) <= creado_hasta)
    return consulta.filter_by(estatus="A").order_by(CitClienteRegistro.id.desc())


def get_cit_cliente_registro(db: Session, cit_cliente_registro_id: int) -> CitClienteRegistro:
    """Consultar un registro de cliente por su id"""
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise CitasNotExistsError("No existe ese registro de cliente")
    if cit_cliente_registro.estatus != "A":
        raise CitasIsDeletedError("No es activo ese registro de cliente, está eliminado")
    return cit_cliente_registro


def get_cit_clientes_registros_cantidades_creados_por_dia(
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
    # Si se recibe creado, se limita a esa fecha
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise CitasOutOfRangeParamError("Creado fuera de rango")
        consulta = consulta.filter(func.date(CitClienteRegistro.creado) == creado)
    else:
        # Si se reciben creado_desde y creado_hasta, validar que sean correctos
        if creado_desde and creado_hasta:
            if creado_desde > creado_hasta:
                raise CitasOutOfRangeParamError("El rango de fechas no es correcto")
        # Si NO se reciben creado_desde y creado_hasta, se limitan a los últimos 30 días
        if creado_desde is None and creado_hasta is None:
            creado_desde = HOY - timedelta(days=30)
            creado_hasta = HOY
        # Si solo se recibe creado_desde, entonces creado_hasta es HOY
        if creado_desde and creado_hasta is None:
            creado_hasta = HOY
        if creado_desde is not None:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise CitasOutOfRangeParamError("Creado desde fuera de rango")
            consulta = consulta.filter(func.date(CitClienteRegistro.creado) >= creado_desde)
        if creado_hasta is not None:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise CitasOutOfRangeParamError("Creado hasta fuera de rango")
            consulta = consulta.filter(func.date(CitClienteRegistro.creado) <= creado_hasta)
    return consulta.group_by(func.date(CitClienteRegistro.creado))
