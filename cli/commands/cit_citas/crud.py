"""
Cit Citas CRUD
"""
from datetime import date
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_cit_citas(
    authorization_header: dict,
    limit: int = LIMIT,
    fecha: date = None,
    cit_cliente_email: str = None,
    oficina_clave: str = None,
    estado: str = None,
) -> Any:
    """Solicitar cit_citas"""
    parametros = {"limit": limit}
    if fecha is not None:
        parametros["fecha"] = fecha
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    if estado is not None:
        parametros["estado"] = estado
    try:
        response = requests.get(
            f"{BASE_URL}/cit_citas",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_citas") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_citas: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_citas") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_citas")
    return data_json


def get_cit_citas_creados_por_dia(
    authorization_header: dict,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Solicitar cantidades de citas creadas por dia"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/cit_citas/creados_por_dia",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_citas") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_citas: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_citas") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_citas")
    return data_json


def get_cit_citas_agendadas_por_oficina_servicio(
    authorization_header: dict,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
) -> Any:
    """Solicitar cantidades de citas agendadas por oficina y servicio"""
    parametros = {}
    if inicio is not None:
        parametros["inicio"] = inicio
    if inicio_desde is not None:
        parametros["inicio_desde"] = inicio_desde
    if inicio_hasta is not None:
        parametros["inicio_hasta"] = inicio_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/cit_citas/agendadas_por_servicio_oficina",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar cit_citas") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar cit_citas: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar cit_citas") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total al solicitar cit_citas")
    return data_json
