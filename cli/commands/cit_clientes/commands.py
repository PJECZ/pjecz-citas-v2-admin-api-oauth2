"""
Cit Clientes Commands
"""
from datetime import datetime

import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_cit_clientes

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
    nombres: str = None,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
):
    """Consultar clientes"""
    try:
        respuesta = get_cit_clientes(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            email=email,
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
