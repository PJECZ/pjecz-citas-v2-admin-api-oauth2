"""
Roles CRUD (create, read, update, and delete)
"""
from typing import Any
import requests

import lib.exceptions


def get_roles(
    base_url: str,
    authorization_header: dict,
    limit: int = 40,
) -> Any:
    """Solicitar roles"""
    parametros = {"limit": limit}
    try:
        response = requests.get(
            f"{base_url}/roles",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar roles") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar roles\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar roles")
    return data_json
