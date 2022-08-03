"""
CLI Cit Clientes Recuperaciones
"""
from datetime import datetime

import requests
import typer
from rich.console import Console
from rich.table import Table

import api
import exceptions

app = typer.Typer()


def get_cit_clientes_recuperaciones(
    base_url: str,
    authorization_header: dict,
    cit_cliente_email: str = None,
    ya_recuperado: bool = None,
) -> dict:
    """Solicitar a la API el listado de recuperaciones de los clientes"""
    parametros = {"limit": 10}
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    if ya_recuperado is not None:
        parametros["ya_recuperado"] = ya_recuperado
    try:
        response = requests.get(
            f"{base_url}/cit_clientes_recuperaciones",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise exceptions.CLIConnectionError("No hay respuesta al obtener las recuperaciones de los clientes") from error
    if response.status_code != 200:
        raise exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise exceptions.CLIResponseError("No se recibio items o total en la respuesta")
    return data_json


@app.command()
def consultar(
    email: str = None,
):
    """Consultar recuperaciones de los clientes"""
    print("Consultar recuperaciones de los clientes")
    try:
        respuesta = get_cit_clientes_recuperaciones(
            base_url=api.base_url(),
            authorization_header=api.authorization(),
            cit_cliente_email=email,
        )
    except exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "creado", "nombre", "email", "expiracion", "mensajes", "ya recuperado")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        expiracion = datetime.strptime(registro["expiracion"], "%Y-%m-%d").date()
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_nombre"],
            registro["cit_cliente_email"],
            expiracion.strftime("%Y-%m-%d"),
            str(registro["mensajes_cantidad"]),
            int(registro["ya_recuperado"]),
            registro["email"],
        )
    console.print(table)


if __name__ == "__main__":
    app()
