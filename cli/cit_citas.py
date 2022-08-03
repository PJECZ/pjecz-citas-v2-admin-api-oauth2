"""
CLI Cit Citas
"""
from datetime import datetime

import requests
import typer
from rich.console import Console
from rich.table import Table

import lib.connections
import lib.exceptions

app = typer.Typer()


def get_cit_citas(
    base_url: str,
    authorization_header: dict,
    cit_cliente_email: str = None,
    oficina_clave: str = None,
    estado: str = None,
) -> dict:
    """Solicitar el listado de citas"""
    parametros = {"limit": 10}
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


@app.command()
def consultar(
    email: str = None,
    oficina: str = None,
    estado: str = None,
):
    """Consultar citas"""
    print("Consultar las citas")
    try:
        respuesta = get_cit_citas(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            cit_cliente_email=email,
            oficina_clave=oficina,
            estado=estado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "oficina", "inicio", "nombre", "servicio", "estado")
    for registro in respuesta["items"]:
        inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
        table.add_row(
            str(registro["id"]),
            registro["oficina_clave"],
            inicio.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_nombre"],
            registro["cit_servicio_clave"],
            registro["estado"],
        )
    console.print(table)


if __name__ == "__main__":
    app()
