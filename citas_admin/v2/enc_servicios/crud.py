"""
Encuestas Servicios v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime

from typing import Any
from sqlalchemy.orm import Session

from config.settings import SERVIDOR_HUSO_HORARIO
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave, safe_email, safe_string

from .models import EncServicio
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente
from ..oficinas.crud import get_oficina
from ..oficinas.models import Oficina


def get_enc_servicios(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar las encuestas de servicios activas"""
    consulta = db.query(EncServicio)

    # Filtrar por el cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(EncServicio.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=True)
        if cit_cliente_email is None or cit_cliente_email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(EncServicio.creado >= desde_dt).filter(EncServicio.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(EncServicio.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(EncServicio.creado <= hasta_dt)

    # Filtrar por estado
    if estado is None:
        consulta = consulta.filter(EncServicio.estado == "CONTESTADO")  # Si no se especifica, se filtra
    else:
        estado = safe_string(estado)
        if estado not in EncServicio.ESTADOS:
            raise CitasNotValidParamError("El estado no es válido")
        consulta = consulta.filter(EncServicio.estado == estado)

    # Filtrar por la oficina
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(EncServicio.oficina == oficina)
    elif oficina_clave is not None:
        oficina_clave = safe_clave(oficina_clave)
        if oficina_clave is None or oficina_clave == "":
            raise CitasNotValidParamError("No es válida la clave de la oficina")
        consulta = consulta.join(Oficina)
        consulta = consulta.filter(Oficina.clave == oficina_clave)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(EncServicio.id)


def get_enc_servicio(db: Session, enc_servicio_id: int) -> EncServicio:
    """Consultar una encuesta de servicio por su id"""
    enc_servicio = db.query(EncServicio).get(enc_servicio_id)
    if enc_servicio is None:
        raise CitasNotExistsError("No existe ese encuesta de servicio")
    if enc_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese encuesta de servicio, está eliminado")
    return enc_servicio
