"""
Encuestas Sistemas v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any, Optional

from hashids import Hashids
import pytz
from sqlalchemy.orm import Session

from config.settings import Settings
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string

from .models import EncSistema
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente


def get_enc_sistemas(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
) -> Any:
    """Consultar los encuestas de sistemas activos"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(EncSistema)

    # Filtrar por el cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(EncSistema.cit_cliente == cit_cliente)
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
        consulta = consulta.filter(EncSistema.creado >= desde_dt).filter(EncSistema.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(EncSistema.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(EncSistema.creado <= hasta_dt)

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado not in EncSistema.ESTADOS:
            raise CitasNotValidParamError("El estado no es válido")
        consulta = consulta.filter(EncSistema.estado == estado)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(EncSistema.id.desc())


def get_enc_sistema(db: Session, enc_sistema_id: int) -> EncSistema:
    """Consultar un encuesta de sistemas por su id"""
    enc_sistema = db.query(EncSistema).get(enc_sistema_id)
    if enc_sistema is None:
        raise CitasNotExistsError("No existe ese encuesta de sistemas")
    if enc_sistema.estatus != "A":
        raise CitasIsDeletedError("No es activo ese encuesta de sistemas, está eliminado")
    return enc_sistema


def get_enc_sistema_url(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
) -> Optional[str]:
    """Obtener la URL de la encuesta de sistema si existe"""

    # Consultar
    enc_servicio = db.query(EncSistema)

    # Filtrar por el cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(EncSistema.cit_cliente == cit_cliente)
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
    enc_servicio = enc_servicio.filter(EncSistema.estado == "PENDIENTE").first()

    # Si no existe, entregar None
    if enc_servicio is None:
        return None

    # Preparar el cifrado
    hashids = Hashids(settings.salt, min_length=8)

    # Entregar la URL
    return f"{settings.poll_system_url}?hashid={hashids.encode(enc_servicio.id)}"
