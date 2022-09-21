"""
Encuestas Servicios v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any, Optional

from hashids import Hashids
import pytz
from sqlalchemy.orm import Session

from config.settings import Settings
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_clave, safe_curp, safe_email, safe_string

from .models import EncServicio
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente
from ..oficinas.crud import get_oficina
from ..oficinas.models import Oficina


def get_enc_servicios(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar las encuestas de servicios activas"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(EncServicio)

    # Filtrar por el cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(EncServicio.cit_cliente == cit_cliente)
    elif cit_cliente_curp is not None:
        curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if curp is None:
            raise CitasNotValidParamError("No es válido el CURP")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.curp == curp)
    elif cit_cliente_email is not None:
        email = safe_email(cit_cliente_email, search_fragment=True)
        if email is None:
            raise CitasNotValidParamError("No es válido el e-mail")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == email)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(EncServicio.creado >= desde_dt).filter(EncServicio.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(EncServicio.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(EncServicio.creado <= hasta_dt)

    # Filtrar por estado
    if estado is not None:
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
        if oficina_clave:
            raise CitasNotValidParamError("No es válida la clave de la oficina")
        consulta = consulta.join(Oficina)
        consulta = consulta.filter(Oficina.clave == oficina_clave)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(EncServicio.id.desc())


def get_enc_servicio(db: Session, enc_servicio_id: int) -> EncServicio:
    """Consultar una encuesta de servicio por su id"""
    enc_servicio = db.query(EncServicio).get(enc_servicio_id)
    if enc_servicio is None:
        raise CitasNotExistsError("No existe ese encuesta de servicio")
    if enc_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese encuesta de servicio, está eliminado")
    return enc_servicio


def get_enc_servicio_url(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
) -> Optional[str]:
    """Obtener la URL de la encuesta de servicio PENDIENTE si existe"""

    # Consultar
    enc_servicio = db.query(EncServicio)

    # Filtrar por el cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(EncServicio.cit_cliente == cit_cliente)
    elif cit_cliente_curp is not None:
        curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if curp is None:
            raise CitasNotValidParamError("No es válido el CURP")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.curp == curp)
    elif cit_cliente_email is not None:
        email = safe_email(cit_cliente_email, search_fragment=True)
        if email is None:
            raise CitasNotValidParamError("No es válido el e-mail")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == email)
    else:
        raise CitasNotValidParamError("No se proporcionó el cliente")

    # Consultar la encuesta de servicio PENDIENTE
    enc_servicio = enc_servicio.filter(EncServicio.estado == "PENDIENTE").first()

    # Si no existe, entregar None
    if enc_servicio is None:
        return None

    # Preparar el cifrado
    hashids = Hashids(settings.salt, min_length=8)

    # Entregar la URL
    return f"{settings.poll_service_url}?hashid={hashids.encode(enc_servicio.id)}"
