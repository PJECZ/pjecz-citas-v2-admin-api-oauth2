"""
Cit Clientes Registros CRUD
"""
from datetime import date, datetime
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_cit_clientes_registros(
    authorization_header: dict,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    limit: int = LIMIT,
    nombres: str = None,
    offset: int = 0,
    registrado: bool = None,
) -> Any:
    """Solicitar el listado de registros de los clientes"""
    parametros = {"limit": limit}
    if apellido_primero is not None:
        parametros["apellido_primero"] = apellido_primero
    if apellido_segundo is not None:
        parametros["apellido_segundo"] = apellido_segundo
    if curp is not None:
        parametros["curp"] = curp
    if email is not None:
        parametros["email"] = email
    if nombres is not None:
        parametros["nombres"] = nombres
    if offset > 0:
        parametros["offset"] = offset
    if registrado is not None:
        parametros["ya_registrado"] = registrado
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


def resend_cit_clientes_registros(
    authorization_header: dict,
) -> Any:
    """Reenviar los mensajes de los registros"""

    # Comparar las fechas de expiracion con la de hoy
    ahora = datetime.now()

    # Inicializar el listado donde se acumulan los mensajes enviados
    enviados = []

    # Comenzar con offset cero
    offset = 0

    # Consultar por primera vez las registros pendientes
    cit_clientes_registros = get_cit_clientes_registros(
        authorization_header=authorization_header,
        registrado=False,
        offset=offset,
    )
    total = cit_clientes_registros["total"]

    # Bucle
    while offset < total:

        # Bucle para procesar resultados de la consulta
        for item in cit_clientes_registros["items"]:

            # Si ya expiró, no se envía y de da de baja
            expiracion = datetime.strptime(item["expiracion"], "%Y-%m-%dT%H:%M:%S.%f")
            if expiracion < ahora:
                # delete_cit_cliente_registro(authorization_header: dict, id=item["expiracion"], )
                continue

            # Acumular
            enviados.append(item)

        # Siguiente consulta
        offset += LIMIT

        # Consultar las recuperaciones pendientes
        cit_clientes_registros = get_cit_clientes_registros(
            authorization_header=authorization_header,
            registrado=False,
            offset=offset,
        )

        # Si ya no hay items, salir del bucle
        if len(cit_clientes_registros["items"]) == 0:
            break

    # Entregar
    return {"items": enviados, "total": len(enviados)}
