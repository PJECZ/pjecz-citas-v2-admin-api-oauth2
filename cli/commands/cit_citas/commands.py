"""
Cit Citas Commands
"""
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

import lib.connections
import lib.exceptions

from .crud import get_cit_citas

app = typer.Typer()


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
