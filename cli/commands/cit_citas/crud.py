"""
Cit Citas CRUD
"""
import requests

import lib.exceptions


def get_cit_citas(
    base_url: str,
    authorization_header: dict,
    limit: int = 40,
    cit_cliente_email: str = None,
    oficina_clave: str = None,
    estado: str = None,
) -> dict:
    """Solicitar el listado de citas"""
    parametros = {"limit": limit}
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
