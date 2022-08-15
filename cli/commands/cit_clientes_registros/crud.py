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
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las recuperaciones de los clientes") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json


def resend_cit_clientes_registros(
    authorization_header: dict,
    cit_cliente_email: str = None,
) -> Any:
    """Reenviar mensajes de las registros de los clientes"""
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
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las registros de los clientes") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
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
            f"{BASE_URL}/cit_clientes_registros/calcular_cantidades_creados_por_dia",
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
