"""
CLI Commands Cit Dias Disponibles Request API
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_cit_dias_disponibles(
    authorization_header: dict,
    limit: int = LIMIT,
) -> Any:
    """Solicitar dias disponibles, entrega un listado de fechas"""
    parametros = {"limit": limit}
    try:
        response = requests.get(
            f"{BASE_URL}/cit_dias_disponibles",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_dias_disponibles") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_dias_disponibles: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_dias_disponibles") from error
    data_json = response.json()
    return data_json


def get_cit_dia_disponible(
    authorization_header: dict,
) -> Any:
    """Solicitar el proximo dia disponible, por ejemplo, si hoy es viernes y el lunes es dia inhabil, entrega el martes"""
    try:
        response = requests.get(
            f"{BASE_URL}/cit_dias_disponibles/proximo",
            headers=authorization_header,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_dias_disponibles") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_dias_disponibles: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_dias_disponibles") from error
    data_json = response.json()
    if "fecha" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio la fecha en la respuesta al solicitar cit_dias_disponibles")
    return data_json
