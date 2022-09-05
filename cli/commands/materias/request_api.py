"""
CLI Commands Materias Request API
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_materias(
    authorization_header: dict,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar materias"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        response = requests.get(
            f"{BASE_URL}/materias",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar materias") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar materias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar materias") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar materias")
    return data_json