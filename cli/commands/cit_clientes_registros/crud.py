"""
Cit Clientes Registros CRUD
"""
from datetime import date
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_cit_clientes_registros(
    authorization_header: dict,
    limit: int = LIMIT,
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    ya_registrado: bool = None,
) -> Any:
    """Solicitar el listado de registros de los clientes"""
    parametros = {"limit": limit}
    if nombres is not None:
        parametros["nombres"] = nombres
    if apellido_primero is not None:
        parametros["apellido_primero"] = apellido_primero
    if apellido_segundo is not None:
        parametros["apellido_segundo"] = apellido_segundo
    if curp is not None:
        parametros["curp"] = curp
    if email is not None:
        parametros["email"] = email
    if ya_registrado is not None:
        parametros["ya_registrado"] = ya_registrado
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes_registros",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes_registros") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_clientes_registros: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_clientes_registros") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_clientes_registros")
    return data_json


def get_cit_clientes_registros_cantidades_creados_por_dia(
    authorization_header: dict,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Solicitar cantidades de registros creados por dia"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes_registros/creados_por_dia",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes_registros") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_clientes_registros: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_clientes_registros") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_clientes_registros")
    return data_json


"""

def resend_cit_clientes_registros(
    authorization_header: dict,
    cit_cliente_email: str = None,
) -> Any:
    Reenviar mensajes de las registros de los clientes
    parametros = {}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes_registros/reenviar_mensajes",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes_registros") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_clientes_registros: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_clientes_registros") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_clientes_registros")
    return data_json


def resend_cit_clientes_registros(
    db: Session,
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
) -> Any:
    Reenviar mensajes de los registros pendientes

    # Consultar los registros pendientes
    consulta = db.query(CitClienteRegistro).filter_by(ya_registrado=False).filter_by(estatus="A")

    # Filtrar por cliente
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
    if email is not None:
        email = safe_email(email, search_fragment=True)
        if email is None or email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.filter(CitClienteRegistro.email.contains(email))

    # Bucle para enviar los mensajes, colocando en la cola de tareas
    enviados = []
    for cit_cliente_registro in consulta.order_by(CitClienteRegistro.id.desc()):

        # Si ya expiró, no se envía y de da de baja
        if cit_cliente_registro.expiracion <= datetime.now():
            cit_cliente_registro.estatus = "B"
            db.add(cit_cliente_registro)
            db.commit()
            continue

        # Enviar el mensaje
        task_queue.enqueue(
            "citas_admin.blueprints.cit_clientes_registros.tasks.enviar",
            cit_cliente_registro_id=cit_cliente_registro.id,
        )

        # Acumular
        enviados.append(CitClienteRegistroOut.from_orm(cit_cliente_registro))

    # Entregar
    return enviados


@cit_clientes_registros.get("/reenviar_mensajes", response_model=Dict)
async def reenviar_mensajes(
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    Reenviar mensajes de las recuperaciones pendientes
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        enviados = resend_cit_clientes_registros(
            db,
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            email=email,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return {"items": enviados, "total": len(enviados)}


"""
