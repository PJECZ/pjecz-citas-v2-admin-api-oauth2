"""
Cit Clientes Recuperaciones Commands
"""
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

import lib.connections
import lib.exceptions

from .crud import get_cit_clientes_recuperaciones, resend_cit_clientes_recuperaciones

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
    email: str = None,
    recuperado: bool = None,
):
    """Consultar recuperaciones de los clientes"""
    print("Consultar recuperaciones de los clientes")
    try:
        respuesta = get_cit_clientes_recuperaciones(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
            cit_cliente_email=email,
            ya_recuperado=recuperado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "creado", "nombre", "email", "expiracion", "mensajes", "recuperado")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        expiracion = datetime.strptime(registro["expiracion"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_nombre"],
            registro["cit_cliente_email"],
            expiracion.strftime("%Y-%m-%d %H:%M:%S"),
            str(registro["mensajes_cantidad"]),
            "YA" if bool(registro["ya_recuperado"]) else "",
        )
    console.print(table)


@app.command()
def reenviar(
    email: str = None,
):
    """Reenviar mensajes de las recuperaciones de los clientes"""
    print("Reenviar mensajes de las recuperaciones de los clientes")
    try:
        respuesta = resend_cit_clientes_recuperaciones(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            cit_cliente_email=email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = Console()
    table = Table("id", "creado", "nombre", "email", "expiracion", "mensajes")
    for registro in respuesta:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        expiracion = datetime.strptime(registro["expiracion"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_nombre"],
            registro["cit_cliente_email"],
            expiracion.strftime("%Y-%m-%d %H:%M:%S"),
            str(registro["mensajes_cantidad"]),
        )
    console.print(table)
