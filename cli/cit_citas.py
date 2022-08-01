"""
CLI Cit Citas
"""
import requests
import typer
from rich.console import Console
from rich.table import Table

import api
import exceptions

app = typer.Typer()


def get_cit_citas(
    base_url: str,
    authorization_header: dict,
    cit_cliente_email: str = None,
    oficina_clave: str = None,
) -> dict:
    """Solicitar a la API el listado de citas"""
    parametros = {"limit": 10}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    try:
        response = requests.get(
            f"{base_url}/cit_citas",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise exceptions.CLIConnectionError("No hay respuesta al obtener las citas") from error
    if response.status_code != 200:
        raise exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json


@app.command()
def consultar():
    """Consultar citas"""
    print("Consultar las citas")
    try:
        respuesta = get_cit_citas(
            base_url=api.base_url(),
            authorization_header=api.authorization(),
        )
    except exceptions.CLIError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "oficina", "inicio", "nombre", "servicio", "estado")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["oficina_clave"],
            registro["inicio"],
            registro["cit_cliente_nombre"],
            registro["cit_servicio_clave"],
            registro["estado"],
        )
    console.print(table)


if __name__ == "__main__":
    app()
