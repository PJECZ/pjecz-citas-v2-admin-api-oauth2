"""
Cit Citas CRUD
"""
from datetime import date

from typing import Any
import requests

import lib.exceptions


def get_cit_citas(
    base_url: str,
    authorization_header: dict,
    limit: int = 40,
    fecha: date = None,
    cit_cliente_email: str = None,
    oficina_clave: str = None,
    estado: str = None,
) -> Any:
    """Solicitar el listado de citas"""
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
            f"{base_url}/cit_citas",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las citas") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json


def get_cit_citas_cantidades_creados_por_dia(
    base_url: str,
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
            f"{base_url}/cit_citas/calcular_cantidades_creados_por_dia",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al obtener las citas") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json


def get_cit_citas_cantidades_agendadas_por_oficina_servicio(
    base_url: str,
    authorization_header: dict,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
) -> Any:
    """Solicitar cantidades de citas agendadas por oficina y servicio"""
