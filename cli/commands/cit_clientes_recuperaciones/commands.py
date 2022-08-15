"""
Cit Clientes Recuperaciones Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_cit_clientes_recuperaciones, get_cit_clientes_recuperaciones_cantidades_creados_por_dia, resend_cit_clientes_recuperaciones

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    email: str = None,
    recuperado: bool = None,
):
    """Consultar recuperaciones de los clientes"""
    rich.print("Consultar recuperaciones de los clientes...")
    try:
        respuesta = get_cit_clientes_recuperaciones(
            authorization_header=authorization_header(),
            limit=limit,
            cit_cliente_email=email,
            ya_recuperado=recuperado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "creado", "nombre", "email", "expiracion", "mensajes", "recuperado")
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
    rich.print(f"Total: [green]{respuesta['total']}[/green] recuperaciones")


@app.command()
def reenviar(
    email: str = None,
    test: bool = True,
):
    """Reenviar mensajes de las recuperaciones de los clientes"""
    rich.print("Reenviar mensajes de las recuperaciones de los clientes...")
    try:
        respuesta = resend_cit_clientes_recuperaciones(
            authorization_header=authorization_header(),
            cit_cliente_email=email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "creado", "nombre", "email", "expiracion", "mensajes")
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
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] mensajes en cola")


@app.command()
def mostrar_cantidades_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de recuperaciones creadas por dia"""
    rich.print("Mostrar cantidades de recuperaciones creadas por dia...")
    try:
        respuesta = get_cit_clientes_recuperaciones_cantidades_creados_por_dia(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("creado", "cantidad")
    for registro in respuesta["items"]:
        table.add_row(
            registro["creado"],
            str(registro["cantidad"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] recuperaciones")
