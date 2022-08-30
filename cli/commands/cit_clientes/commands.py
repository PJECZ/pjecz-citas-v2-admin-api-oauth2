"""
Cit Clientes Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_cit_clientes, get_cit_clientes_creados_por_dia

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
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "creado", "nombres", "apellido pri", "apellido seg", "curp", "email", "md5", "sha256")
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
    rich.print(f"Total: [green]{respuesta['total']}[/green] clientes")
