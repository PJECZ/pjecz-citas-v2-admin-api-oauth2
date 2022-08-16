"""
Cit Dias Disponibles Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_cit_dias_disponibles, get_cit_dia_disponible

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
):
    """Consultar dias disponibles"""
    rich.print("Consultar dias disponibles...")
    try:
        respuesta = get_cit_dias_disponibles(
            authorization_header=authorization_header(),
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
    """Consultar proximo dia hábil"""
    rich.print("Consultar proximo dia hábil...")
    try:
        respuesta = get_cit_dia_disponible(
            authorization_header=authorization_header(),
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(f"Proximo dia hábil: [green]{respuesta['fecha']}[/green]")
