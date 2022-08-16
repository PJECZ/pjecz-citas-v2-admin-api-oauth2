"""
Oficinas CRUD (create, read, update, and delete)
"""
from typing import Any
import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_oficinas(
    authorization_header: dict,
    limit: int = LIMIT,
    distrito_id: int = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    puede_agendar_citas: bool = None,
) -> Any:
    """Solicitar oficinas"""
    parametros = {"limit": limit}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if domicilio_id is not None:
        parametros["domicilio_id"] = domicilio_id
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    if puede_agendar_citas is not None:
        parametros["puede_agendar_citas"] = puede_agendar_citas
    try:
        response = requests.get(
            f"{BASE_URL}/oficinas",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar oficinas") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar oficinas\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar oficinas")
    return data_json
