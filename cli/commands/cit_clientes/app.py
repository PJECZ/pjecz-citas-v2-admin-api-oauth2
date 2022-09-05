"""
CLI Commands Cit Clientes App
"""
from datetime import datetime

import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
from lib.exceptions import CLIAnyError

from .request_api import get_cit_clientes, get_cit_clientes_creados_por_dia

app = typer.Typer()


@app.command()
def consultar(
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    limit: int = LIMIT,
    nombres: str = None,
    offset: int = 0,
):
    """Consultar clientes"""
    rich.print("Consultar clientes...")
    try:
        respuesta = get_cit_clientes(
            authorization_header=authorization_header(),
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            email=email,
            limit=limit,
            nombres=nombres,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Nombres", "A. Primero", "A. Segundo", "CURP", "e-mail", "MD5", "SHA256")
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
            "" if registro["contrasena_md5"] == "" else "****",
            "" if registro["contrasena_sha256"] == "" else "****",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] clientes")


@app.command()
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de clientes creados por dia"""
    rich.print("Mostrar cantidades de clientes creados por dia...")
    try:
        respuesta = get_cit_clientes_creados_por_dia(
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
    rich.print(f"Total: [green]{respuesta['total']}[/green] clientes")
