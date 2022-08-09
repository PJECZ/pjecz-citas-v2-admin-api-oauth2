"""
Cit Clientes Registros Commands
"""
from datetime import datetime

import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_cit_clientes_registros, get_cit_clientes_registros_cantidades_creados_por_dia, resend_cit_clientes_registros

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    registrado: bool = None,
):
    """Consultar registros de los clientes"""
    rich.print("Consultar registros de los clientes...")
    try:
        respuesta = get_cit_clientes_registros(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            email=email,
            ya_registrado=registrado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "creado", "nombres", "apellido_primero", "apellido_segundo", "curp", "email", "expiracion", "mensajes", "registrado")
    for registro in respuesta["items"]:
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
            expiracion.strftime("%Y-%m-%d %H:%M:%S"),
            str(registro["mensajes_cantidad"]),
            "YA" if bool(registro["ya_registrado"]) else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] registros")


@app.command()
def reenviar(
    email: str = None,
):
    """Reenviar mensajes de las registros de los clientes"""
    rich.print("Reenviar mensajes de las registros de los clientes...")
    try:
        respuesta = resend_cit_clientes_registros(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            cit_cliente_email=email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "creado", "nombres", "apellido_primero", "apellido_segundo", "curp", "email", "expiracion", "mensajes")
    for registro in respuesta["items"]:
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
    """Mostrar cantidades de registros creados por dia"""
    rich.print("Mostrar cantidades de registros creados por dia...")
    try:
        respuesta = get_cit_clientes_registros_cantidades_creados_por_dia(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
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
    rich.print(f"Total: [green]{respuesta['total']}[/green] registros")
