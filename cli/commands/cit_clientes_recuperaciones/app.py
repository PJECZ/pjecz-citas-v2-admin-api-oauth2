"""
CLI Commands Cit Clientes Recuperaciones App
"""
from datetime import datetime

import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
from lib.exceptions import CLIAnyError

from .request_api import get_cit_clientes_recuperaciones, get_cit_clientes_recuperaciones_creados_por_dia

app = typer.Typer()


@app.command()
def consultar(
    email: str = None,
    limit: int = LIMIT,
    recuperado: bool = False,
    offset: int = 0,
):
    """Consultar recuperaciones de los clientes"""
    rich.print("Consultar recuperaciones de los clientes...")
    try:
        respuesta = get_cit_clientes_recuperaciones(
            authorization_header=authorization_header(),
            email=email,
            limit=limit,
            recuperado=recuperado,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Nombre", "e-mail", "Expiracion", "Mensajes", "Recuperado")
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
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de recuperaciones creadas por dia"""
    rich.print("Mostrar cantidades de recuperaciones creadas por dia...")
    try:
        respuesta = get_cit_clientes_recuperaciones_creados_por_dia(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table()
    table.add_column("Creado")
    table.add_column("Cantidad", justify="right")
    for creado, cantidad in respuesta["items"].items():
        table.add_row(creado, str(cantidad))
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] recuperaciones")


@app.command()
def reenviar(
    test: bool = True,
):
    """Reenviar mensajes de las recuperaciones de los clientes"""
    rich.print("Reenviar mensajes de las recuperaciones de los clientes...")
