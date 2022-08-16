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
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las recuperaciones de los clientes") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
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
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las recuperaciones de los clientes") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
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
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las citas") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json
