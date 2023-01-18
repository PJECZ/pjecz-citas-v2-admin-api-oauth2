"""
Pagos Pagos v2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session

from config.settings import Settings
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string, safe_telefono

from .models import PagPago
from .schemas import PagCarroIn, OnePagCarroOut, PagResultadoIn, OnePagResultadoOut
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente
from ..pag_tramites_servicios.crud import get_pag_tramite_servicio_from_clave


def get_pag_pagos(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    pag_tramite_servicio_id: int = None,
    estado: str = None,
    estatus: str = None,
    ya_se_envio_comprobante: bool = None,
) -> Any:
    """Consultar los pagos activos"""

    # Consulta
    consulta = db.query(PagPago)

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(PagPago.cit_cliente == cit_cliente)
    elif cit_cliente_curp is not None:
        cit_cliente_curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if cit_cliente_curp is None or cit_cliente_curp == "":
            raise CitasNotValidParamError("No es válido el CURP")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.curp == cit_cliente_curp)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=False)
        if cit_cliente_email is None or cit_cliente_email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por tramite y servicio
    if pag_tramite_servicio_id is not None:
        consulta = consulta.filter_by(pag_tramite_servicio_id=pag_tramite_servicio_id)

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado in PagPago.ESTADOS:
            consulta = consulta.filter_by(estado=estado)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por ya_se_envio_comprobante
    if ya_se_envio_comprobante is not None:
        consulta = consulta.filter_by(ya_se_envio_comprobante=ya_se_envio_comprobante)

    # Entregar
    return consulta.order_by(PagPago.id)


def get_pag_pago(db: Session, pag_pago_id: int) -> PagPago:
    """Consultar un pago por su id"""
    pag_pago = db.query(PagPago).get(pag_pago_id)
    if pag_pago is None:
        raise CitasNotExistsError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise CitasIsDeletedError("No es activo ese pago, está eliminado")
    return pag_pago


def create_payment(
    db: Session,
    settings: Settings,
    datos: PagCarroIn,
) -> OnePagCarroOut:
    """Crear un pago"""

    # Validar nombres
    nombres = safe_string(datos.nombres)
    if nombres is None:
        raise CitasNotValidParamError("El nombre no es valido")

    # Validar apellido_primero
    apellido_primero = safe_string(datos.apellido_primero)
    if apellido_primero is None:
        raise CitasNotValidParamError("El apellido primero no es valido")

    # Validar apellido_segundo
    apellido_segundo = safe_string(datos.apellido_segundo)
    if apellido_segundo is None:
        raise CitasNotValidParamError("El apellido segundo no es valido")

    # Validar curp
    curp = safe_curp(datos.curp)
    if curp is None:
        raise CitasNotValidParamError("El CURP no es valido")

    # Validar email
    email = safe_email(datos.email)
    if email is None:
        raise CitasNotValidParamError("El correo electronico no es valido")

    # Validar telefono
    telefono = safe_telefono(datos.telefono)
    if telefono is None:
        raise CitasNotValidParamError("El telefono no es valido")

    # Validar pag_tramite_servicio_clave
    try:
        pag_tramite_servicio = get_pag_tramite_servicio_from_clave(db, datos.pag_tramite_servicio_clave)
    except (CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError) as error:
        raise error

    # Buscar cliente
    cit_cliente = None
    si_existe = False
    try:
        cit_cliente = get_cit_cliente(db, cit_cliente_curp=curp, cit_cliente_email=email)
        si_existe = True
    except CitasNotExistsError:
        si_existe = False
    except (CitasIsDeletedError, CitasNotValidParamError) as error:
        raise error

    # Si no se encuentra el cliente, crearlo
    if not si_existe:
        renovacion_fecha = datetime.now() + timedelta(days=60)
        cit_cliente = CitCliente(
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            telefono=telefono,
            email=email,
            contrasena_md5="",
            contrasena_sha256="",
            renovacion=renovacion_fecha.date(),
            limite_citas_pendientes=settings.limite_citas_pendientes,
        )
        db.add(cit_cliente)
        db.commit()
        db.refresh(cit_cliente)
        si_existe = True

    # Insertar pago
    pag_pago = PagPago(
        cit_cliente=cit_cliente,
        pag_tramite_servicio=pag_tramite_servicio,
        estado="SOLICITADO",
        email=email,
        folio="",
        total=pag_tramite_servicio.costo,
        ya_se_envio_comprobante=False,
    )
    db.add(pag_pago)
    db.commit()
    db.refresh(pag_pago)

    # TODO: Establecer URL del banco
    url = "https://www.noexiste.com.mx/"

    # Entregar
    return OnePagCarroOut(
        pag_pago_id=pag_pago.id,
        descripcion=pag_tramite_servicio.descripcion,
        email=email,
        monto=pag_pago.total,
        url=url,
    )


def update_payment(
    db: Session,
    datos: PagResultadoIn,
) -> Any:
    """Actualizar un pago"""

    # Validar el XML que mando el banco
    if datos.xml_encriptado.strip() == "":
        raise CitasNotValidParamError("El XML está vacío")

    # Desencriptar el XML que mando el banco

    # TODO: Al desencriptar el XML, se obtiene el id del pago
    pag_pago_id = 1

    # Consultar el pago
    pag_pago = db.query(PagPago).get(pag_pago_id)

    # Validar el pago
    if pag_pago is None:
        raise IndexError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise IndexError("No es activo ese pago, está eliminado")
    if pag_pago.estado != "SOLICITADO":
        raise IndexError("No es un pago solicitado al banco, ya fue procesado")

    # TODO: Al desencriptar el XML, se obtiene el folio y se determina el estado
    estado = "SOLICITADO"
    folio = "0001"

    # Actualizar el pago
    pag_pago.estado = estado
    pag_pago.folio = folio
    db.add(pag_pago)
    db.commit()
    db.refresh(pag_pago)

    # Entregar
    return OnePagResultadoOut(
        pag_pago_id=pag_pago.id,
        nombres=pag_pago.cit_cliente.nombres,
        apellido_primero=pag_pago.cit_cliente.apellido_primero,
        apellido_segundo=pag_pago.cit_cliente.apellido_segundo,
        email=pag_pago.email,
        estado=pag_pago.estado,
        folio=pag_pago.folio,
        total=pag_pago.total,
    )
