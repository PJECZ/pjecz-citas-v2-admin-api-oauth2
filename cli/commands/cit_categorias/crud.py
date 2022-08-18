"""
Cit Categorias CRUD (create, read, update, and delete)
"""
from typing import Any
import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_cit_categorias(
    authorization_header: dict,
    limit: int = LIMIT,
) -> Any:
    """Solicitar cit_categorias"""
    parametros = {"limit": limit}
    try:
        response = requests.get(
            f"{BASE_URL}/cit_categorias",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_categorias") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_categorias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_categorias") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar cit_categorias")
    return data_json
