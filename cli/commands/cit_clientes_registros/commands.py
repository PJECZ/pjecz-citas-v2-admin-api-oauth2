"""
Cit Clientes Registros Commands
"""
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

import lib.connections
import lib.exceptions

from .crud import get_cit_clientes_registros, resend_cit_clientes_registros

app = typer.Typer()


@app.command()
def consultar(
    email: str = None,
):
    """Consultar registros de los clientes"""
    try:
        respuesta = get_cit_clientes_registros(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            email=email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "creado", "nombres", "apellido_primero", "apellido_segundo", "curp", "email", "expiracion", "ya_registrado")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        expiracion = datetime.strptime(registro["expiracion"], "%Y-%m-%d").date()
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["nombres"],
            registro["apellido_primero"],
            registro["apellido_segundo"],
            registro["curp"],
            registro["email"],
            expiracion.strftime("%Y-%m-%d"),
            int(registro["ya_recuperado"]),
        )
    console.print(table)


@app.command()
def reenviar(
    email: str = None,
):
    """Reenviar mensajes de las registros de los clientes"""
    print("Reenviar mensajes de las registros de los clientes")
    try:
        respuesta = resend_cit_clientes_registros(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            cit_cliente_email=email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "creado", "nombres", "apellido_primero", "apellido_segundo", "curp", "email", "expiracion", "mensajes")
    for registro in respuesta:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        expiracion = datetime.strptime(registro["expiracion"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["nombres"],
            registro["apellido_primero"],
            registro["apellido_segundo"],
            registro["curp"],
            registro["email"],
            expiracion.strftime("%Y-%m-%d"),
            int(registro["ya_recuperado"]),
        )
    console.print(table)
