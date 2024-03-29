"""
Cit Citas v2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time, timedelta
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import pytz

from config.settings import Settings
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError, CitasOutOfRangeParamError
from lib.pwgen import generar_codigo_asistencia
from lib.safe_string import safe_clave, safe_curp, safe_email, safe_string

from .models import CitCita
from ..cit_citas_anonimas.crud import get_cit_citas_anonimas
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente
from ..cit_dias_disponibles.crud import get_cit_dias_disponibles
from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles
from ..cit_horas_disponibles.crud import get_cit_horas_disponibles
from ..cit_oficinas_servicios.crud import get_cit_oficinas_servicios
from ..cit_servicios.crud import get_cit_servicio
from ..cit_servicios.models import CitServicio
from ..distritos.crud import get_distrito
from ..distritos.models import Distrito
from ..oficinas.crud import get_oficina
from ..oficinas.models import Oficina


def get_cit_citas(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    estatus: str = None,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(CitCita.cit_cliente == cit_cliente)
    elif cit_cliente_curp is not None:
        cit_cliente_curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if cit_cliente_curp is None:
            raise CitasNotValidParamError("No es válido el CURP")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.curp == cit_cliente_curp)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=False)
        if cit_cliente_email is None:
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por servicio
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitCita.cit_servicio == cit_servicio)
    elif cit_servicio_clave is not None:
        cit_servicio_clave = safe_clave(cit_servicio_clave)
        if cit_servicio_clave is None:
            raise CitasNotValidParamError("No es válida la clave del servicio")
        consulta = consulta.join(CitServicio)
        consulta = consulta.filter(CitServicio.clave == cit_servicio_clave)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por inicio
    if inicio is not None:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    else:
        if inicio_desde is not None:
            desde_dt = datetime(year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta is not None:
            hasta_dt = datetime(year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitCita.inicio <= hasta_dt)

    # Filtrar por estado
    if estado is None:
        consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))  # Si no se especifica, se filtra
    else:
        estado = safe_string(estado)
        if estado not in CitCita.ESTADOS:
            raise CitasNotValidParamError("El estado no es válido")
        consulta = consulta.filter(CitCita.estado == estado)

    # Filtrar por oficina
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitCita.oficina == oficina)
    elif oficina_clave is not None:
        oficina_clave = safe_clave(oficina_clave)
        if oficina_clave is None:
            raise CitasNotValidParamError("No es válida la clave de la oficina")
        consulta = consulta.join(Oficina)
        consulta = consulta.filter(Oficina.clave == oficina_clave)
    consulta = consulta.filter_by(estatus="A")

    # Ordenar
    if cit_cliente_id is not None or cit_cliente_curp is not None or cit_cliente_email is not None or inicio is not None or inicio_desde is not None or inicio_hasta is not None:
        consulta = consulta.order_by(CitCita.inicio)
    else:
        consulta = consulta.order_by(CitCita.id.desc())

    # Entregar
    return consulta


def get_cit_cita(
    db: Session,
    cit_cita_id: int,
) -> CitCita:
    """Consultar un cita por su id"""
    cit_cita = db.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise CitasNotExistsError("No existe ese cita")
    if cit_cita.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cita, está eliminado")
    return cit_cita


def get_cit_citas_creados_por_dia(
    db: Session,
    settings: Settings,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    distrito_id: int = None,
    size: int = 100,
) -> Any:
    """Calcular las cantidades de citas creados por dia"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Iniciar la consulta
    consulta = db.query(
        func.date(CitCita.creado).label("creado"),
        func.count(CitCita.id).label("cantidad"),
    )

    # Si se recibe distrito_id, se filtra por distrito
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.select_from(CitCita).join(Oficina)
        consulta = consulta.filter(Oficina.distrito == distrito)

    # Filtrar estados ASISTIO y PENDIENTE
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))

    # Si NO se reciben creados, se limitan a los últimos "size" días
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy_servidor = datetime.now(servidor_huso_horario)
        hoy = hoy_servidor.astimezone(local_huso_horario).date()
        creado_desde = hoy - timedelta(days=size - 1)
        creado_hasta = hoy

    # Si se recibe creado, se limita a esa fecha
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por la fecha de creacion y entregar
    return consulta.group_by(func.date(CitCita.creado)).order_by(func.date(CitCita.creado))


def get_cit_citas_creados_por_dia_distrito(
    db: Session,
    settings: Settings,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Calcular las cantidades de citas creados por dia y por distrito"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Iniciar la consulta
    consulta = db.query(
        func.date(CitCita.creado).label("creado"),
        Distrito.nombre_corto.label("distrito"),
        func.count(CitCita.id).label("cantidad"),
    )

    # Juntar con oficinas y distritos
    consulta = consulta.select_from(CitCita).join(Oficina).join(Distrito)

    # Filtrar estados ASISTIO y PENDIENTE
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))

    # Si NO se reciben creados, se limitan a los últimos "size" días
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy_servidor = datetime.now(servidor_huso_horario)
        hoy = hoy_servidor.astimezone(local_huso_horario).date()
        creado_desde = hoy - timedelta(days=size - 1)
        creado_hasta = hoy

    # Si se recibe creado, se limita a esa fecha
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por la fecha de creacion y entregar
    consulta = consulta.group_by(func.date(CitCita.creado), Distrito.nombre_corto)

    # Ordenar y entregar
    return consulta.order_by(func.date(CitCita.creado), Distrito.nombre_corto)


def get_cit_citas_agendadas_por_servicio_oficina(
    db: Session,
    settings: Settings,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    size: int = 100,
) -> Any:
    """Calcular las cantidades de citas agendadas por servicio y oficina"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

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

    # Si NO se reciben inicios, se limitan a los últimos "size" días
    if inicio is None and inicio_desde is None and inicio_hasta is None:
        hoy_servidor = datetime.now(servidor_huso_horario)
        hoy = hoy_servidor.astimezone(local_huso_horario).date()
        inicio_desde = hoy - timedelta(days=size - 1)
        inicio_hasta = hoy

    # Si se recibe inicio, se limita a esa fecha
    if inicio is not None:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    if inicio is None and inicio_desde is not None:
        desde_dt = datetime(year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.inicio >= desde_dt)
    if inicio is None and inicio_hasta is not None:
        hasta_dt = datetime(year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.inicio <= hasta_dt)

    # Agrupar por oficina y servicio y entregar
    return consulta.group_by(Oficina.clave, CitServicio.clave).order_by(Oficina.clave, CitServicio.clave)


def create_cit_cita(
    db: Session,
    cit_cliente_id: int,
    cit_servicio_id: int,
    fecha: date,
    hora_minuto: time,
    oficina_id: int,
    notas: str,
    settings: Settings,
) -> Any:
    """Crear una cita"""

    # Consultar el cliente
    cit_cliente = get_cit_cliente(db=db, cit_cliente_id=cit_cliente_id)

    # Consultar la oficina
    oficina = get_oficina(db=db, oficina_id=oficina_id)

    # Consultar el servicio
    cit_servicio = get_cit_servicio(db=db, cit_servicio_id=cit_servicio_id)

    # Validar que ese servicio lo ofrezca esta oficina
    cit_oficinas_servicios = get_cit_oficinas_servicios(db=db, oficina_id=oficina_id).all()
    if cit_servicio_id not in [cit_oficina_servicio.cit_servicio_id for cit_oficina_servicio in cit_oficinas_servicios]:
        raise CitasNotValidParamError("No es posible agendar este servicio en esta oficina")

    # Validar la fecha, debe ser un dia disponible
    if fecha not in get_cit_dias_disponibles(db=db, settings=settings):
        raise CitasNotValidParamError("No es valida la fecha")

    # Validar la hora_minuto, respecto a las horas disponibles
    if hora_minuto not in get_cit_horas_disponibles(db=db, cit_servicio_id=cit_servicio_id, fecha=fecha, oficina_id=oficina_id, settings=settings):
        raise CitasOutOfRangeParamError("No es valida la hora-minuto porque no esta disponible")

    # Validar que las citas en ese tiempo para esa oficina NO hayan llegado al limite de personas
    cit_citas_anonimas = get_cit_citas_anonimas(db=db, fecha=fecha, hora_minuto=hora_minuto, oficina_id=oficina_id)
    if cit_citas_anonimas.count() >= oficina.limite_personas:
        raise CitasOutOfRangeParamError("No se puede crear la cita porque ya se alcanzo el limite de personas en la oficina")

    # Validar que la cantidad de citas con estado PENDIENTE no haya llegado al limite de este cliente
    if get_cit_citas_disponibles_cantidad(db=db, cit_cliente_id=cit_cliente.id, settings=settings) <= 0:
        raise CitasOutOfRangeParamError("No se puede crear la cita porque ya se alcanzo el limite de citas pendientes")

    # Definir los tiempos de la cita
    inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute)
    termino_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute) + timedelta(hours=cit_servicio.duracion.hour, minutes=cit_servicio.duracion.minute)

    # Validar que no tenga una cita pendiente en la misma fecha y hora
    cit_citas = get_cit_citas(db=db, cit_cliente_id=cit_cliente_id, estado="PENDIENTE", settings=settings)
    for cit_cita in cit_citas.all():
        if cit_cita.inicio == inicio_dt:
            raise CitasOutOfRangeParamError("No se puede crear la cita porque ya tiene una cita pendiente en la misma fecha y hora")

    # Definir cancelar_antes con 24 horas antes de la cita
    cancelar_antes = inicio_dt - timedelta(hours=24)

    # Si cancelar_antes es un dia inhabil, domingo o sabado, se busca el dia habil anterior
    dias_inhabiles = get_cit_dias_inhabiles(db=db).all()
    while cancelar_antes.date() in dias_inhabiles or cancelar_antes.weekday() == 6 or cancelar_antes.weekday() == 5:
        if cancelar_antes.date() in dias_inhabiles:
            cancelar_antes = cancelar_antes - timedelta(days=1)
        if cancelar_antes.weekday() == 6:  # Si es domingo, se cambia a viernes
            cancelar_antes = cancelar_antes - timedelta(days=2)
        if cancelar_antes.weekday() == 5:  # Si es sábado, se cambia a viernes
            cancelar_antes = cancelar_antes - timedelta(days=1)

    # Insertar registro
    cit_cita = CitCita(
        cit_servicio_id=cit_servicio.id,
        cit_cliente_id=cit_cliente_id,
        oficina_id=oficina.id,
        inicio=inicio_dt,
        termino=termino_dt,
        notas=safe_string(input_str=notas, max_len=512),
        estado="PENDIENTE",
        asistencia=False,
        codigo_asistencia=generar_codigo_asistencia(),
        cancelar_antes=cancelar_antes,
    )
    db.add(cit_cita)
    db.commit()
    db.refresh(cit_cita)

    # TODO: Agregar tarea en el fondo para que se envie un mensaje via correo electronico

    # Entregar
    return cit_cita


def get_cit_citas_pendientes(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
) -> Any:
    """Consultar las citas PENDIENTE de un cliente"""

    # Consultar y validad al cliente
    cit_cliente = get_cit_cliente(
        db=db,
        cit_cliente_id=cit_cliente_id,
        cit_cliente_curp=cit_cliente_curp,
        cit_cliente_email=cit_cliente_email,
    )

    # Consultar las citas PENDIENTES en el futuro
    return get_cit_citas(
        db=db,
        cit_cliente_id=cit_cliente.id,
        estado="PENDIENTE",
        inicio_desde=date.today(),
        settings=settings,
    )


def get_cit_citas_disponibles_cantidad(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
) -> int:
    """Consultar la cantidad de citas que puede agendar (que es su limite menos las pendientes)"""

    # Consultar el cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id, cit_cliente_curp=cit_cliente_curp, cit_cliente_email=cit_cliente_email)

    # Definir la cantidad limite de citas del cliente
    limite = settings.limite_citas_pendientes
    if cit_cliente.limite_citas_pendientes > limite:
        limite = cit_cliente.limite_citas_pendientes

    # Consultar las citas PENDIENTES
    citas_pendientes_cantidad = get_cit_citas_pendientes(db=db, cit_cliente_id=cit_cliente.id, settings=settings).count()

    # Entregar la cantidad de citas disponibles que puede agendar
    if citas_pendientes_cantidad >= limite:
        return 0
    return limite - citas_pendientes_cantidad


def cancel_cit_cita(
    db: Session,
    cit_cita_id: int,
    cit_cliente_id: int,
) -> CitCita:
    """Cancelar una cita"""

    # Consultar la cita
    cit_cita = get_cit_cita(db=db, cit_cita_id=cit_cita_id)

    # Validar que la cita sea del cliente
    if cit_cita.cit_cliente_id != cit_cliente_id:
        raise CitasNotExistsError("La cita no es de Usted")

    # Validar que no este cancelada
    if cit_cita.estado == "CANCELO":
        raise CitasNotExistsError("Ya esta cancelada esta cita")

    # Validar que se pueda cancelar
    if cit_cita.puede_cancelarse is False:
        raise CitasNotExistsError("No se puede cancelar esta cita")

    # Actualizar registro
    cit_cita.estado = "CANCELO"
    db.add(cit_cita)
    db.commit()
    db.refresh(cit_cita)

    # TODO: Agregar tarea en el fondo para que se envie un mensaje via correo electronico

    # Entregar
    return cit_cita
