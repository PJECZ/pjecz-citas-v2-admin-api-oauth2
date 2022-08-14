"""
Cit Dias Disponibles Typer Commands
"""
import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_cit_dias_disponibles, get_cit_dia_disponible

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
):
    """Consultar dias disponibles"""
    rich.print("Consultar dias disponibles...")
    try:
        respuesta = get_cit_dias_disponibles(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("Fecha")
    for registro in respuesta:
        table.add_row(
            registro["fecha"],
        )
    console.print(table)


@app.command()
def proximo():
    """Consultar proximo dia disponible"""
    rich.print("Consultar proximo dia disponible...")
    try:
        respuesta = get_cit_dia_disponible(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(f"Proxima fecha: [green]{respuesta['fecha']}[/green]")
