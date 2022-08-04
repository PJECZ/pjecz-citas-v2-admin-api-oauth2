"""
Cit Clientes Recuperaciones CRUD
"""
import requests

import lib.exceptions


def get_cit_clientes_recuperaciones(
    base_url: str,
    authorization_header: dict,
    limit: int = 40,
    cit_cliente_email: str = None,
    ya_recuperado: bool = None,
) -> dict:
    """Solicitar el listado de recuperaciones de los clientes"""
    parametros = {"limit": limit}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    if ya_recuperado is not None:
        parametros["ya_recuperado"] = ya_recuperado
    try:
        response = requests.get(
            f"{base_url}/cit_clientes_recuperaciones",
            headers=authorization_header,
            params=parametros,
            timeout=12,
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
    base_url: str,
    authorization_header: dict,
    cit_cliente_email: str = None,
) -> dict:
    """Reenviar mensajes de las recuperaciones de los clientes"""
    parametros = {}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    try:
        response = requests.get(
            f"{base_url}/cit_clientes_recuperaciones/reenviar",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las recuperaciones de los clientes") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    return data_json
