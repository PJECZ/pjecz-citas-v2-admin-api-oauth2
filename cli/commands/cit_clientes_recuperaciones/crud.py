"""
Cit Clientes Recuperaciones CRUD
"""
from datetime import date
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_cit_clientes_recuperaciones(
    authorization_header: dict,
    limit: int = LIMIT,
    cit_cliente_email: str = None,
    ya_recuperado: bool = None,
) -> Any:
    """Solicitar el listado de recuperaciones de los clientes"""
    parametros = {"limit": limit}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    if ya_recuperado is not None:
        parametros["ya_recuperado"] = ya_recuperado
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes_recuperaciones",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes_recuperaciones") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_clientes_recuperaciones: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_clientes_recuperaciones") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_clientes_recuperaciones")
    return data_json


def resend_cit_clientes_recuperaciones(
    authorization_header: dict,
    cit_cliente_email: str = None,
) -> Any:
    """Reenviar mensajes de las recuperaciones de los clientes"""
    parametros = {}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes_recuperaciones/reenviar_mensajes",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes_recuperaciones") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_clientes_recuperaciones: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_clientes_recuperaciones") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_clientes_recuperaciones")
    return data_json


def get_cit_clientes_recuperaciones_cantidades_creados_por_dia(
    authorization_header: dict,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Solicitar cantidades de recuperaciones creadas por dia"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes_recuperaciones/calcular_cantidades_creados_por_dia",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes_recuperaciones") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_clientes_recuperaciones: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_clientes_recuperaciones") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_clientes_recuperaciones")
    return data_json


"""
def resend_cit_clientes_recuperaciones(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    Reenviar mensajes de las recuperaciones pendientes

    # Consultar las recuperaciones pendientes
    consulta = db.query(CitClienteRecuperacion).filter_by(ya_recuperado=False).filter_by(estatus="A")

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, get_cit_cliente)
        consulta = consulta.filter(CitClienteRecuperacion.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=True)
        if cit_cliente_email is None or cit_cliente_email == "":
            raise CitasNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por fecha de creación
    if creado_desde is not None:
        consulta = consulta.filter(func.date(CitClienteRecuperacion.creado) >= creado_desde)
    if creado_hasta is not None:
        consulta = consulta.filter(func.date(CitClienteRecuperacion.creado) <= creado_hasta)

    # Bucle para enviar los mensajes, colocando en la cola de tareas
    enviados = []
    for cit_cliente_recuperacion in consulta.order_by(CitClienteRecuperacion.id).all():

        # Si ya expiró, no se envía y de da de baja
        if cit_cliente_recuperacion.expiracion <= datetime.now():
            cit_cliente_recuperacion.estatus = "B"
            db.commit()
            continue

        # Enviar el mensaje
        task_queue.enqueue(
            "citas_admin.blueprints.cit_clientes_recuperaciones.tasks.enviar",
            cit_cliente_recuperacion_id=cit_cliente_recuperacion.id,
        )

        # Acumular
        enviados.append(CitClienteRecuperacionOut.from_orm(cit_cliente_recuperacion))

    # Entregar
    return enviados

@cit_clientes_recuperaciones.get("/reenviar_mensajes", response_model=Dict)
async def reenviar_mensajes(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    Reenviar mensajes de las recuperaciones pendientes
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        enviados = resend_cit_clientes_recuperaciones(
            db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except CitasAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return {"items": enviados, "total": len(enviados)}


"""
