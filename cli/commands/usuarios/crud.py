"""
Usuarios CRUD (create, read, update, and delete)
"""
from typing import Any
import requests

import lib.exceptions


def get_usuarios(
    base_url: str,
    authorization_header: dict,
    limit: int = 40,
    autoridad_id: int = None,
    oficina_id: int = None,
) -> Any:
    """Solicitar usuarios"""
    parametros = {"limit": limit}
    if autoridad_id is not None:
        parametros["param_str"] = autoridad_id
    if oficina_id is not None:
        parametros["param_str"] = oficina_id
    try:
        response = requests.get(
            f"{base_url}/usuarios",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar usuarios") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar usuarios\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar usuarios")
    return data_json
