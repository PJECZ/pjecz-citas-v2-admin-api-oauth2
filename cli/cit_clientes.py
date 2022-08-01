"""
CLI Cit Clientes
"""
from datetime import datetime

import requests
import typer
from rich.console import Console
from rich.table import Table

import api
import exceptions

app = typer.Typer()


def get_cit_clientes(
    base_url: str,
    authorization_header: dict,
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
) -> dict:
    """Solicitar a la API el listado de clientes"""
    parametros = {"limit": 10}
    if nombres is not None:
        parametros["nombres"] = nombres
    if apellido_primero is not None:
        parametros["apellido_primero"] = apellido_primero
    if apellido_segundo is not None:
        parametros["apellido_segundo"] = apellido_segundo
    if curp is not None:
        parametros["curp"] = curp
    if email is not None:
        parametros["email"] = email
    try:
        response = requests.get(
            f"{base_url}/cit_clientes",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise exceptions.CLIConnectionError("No hay respuesta al obtener los clientes") from error
    if response.status_code != 200:
        raise exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json


@app.command()
def consultar(nombres: str = None, apellido_primero: str = None, apellido_segundo: str = None, curp: str = None, email: str = None):
    """Consultar clientes"""
    print("Consultar los clientes")
    try:
        respuesta = get_cit_clientes(
            base_url=api.base_url(),
            authorization_header=api.authorization(),
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            email=email,
        )
    except exceptions.CLIError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "creado", "nombres", "apellido_primero", "apellido_segundo", "curp", "email")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["nombres"],
            registro["apellido_primero"],
            registro["apellido_segundo"],
            registro["curp"],
            registro["email"],
        )
    console.print(table)


if __name__ == "__main__":
    app()
