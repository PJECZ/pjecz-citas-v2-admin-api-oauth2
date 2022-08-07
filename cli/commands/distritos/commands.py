"""
Distritos Typer Commands
"""
import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_distritos

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
):
    """Consultar distritos"""
    rich.print("Consultar distritos...")
    try:
        respuesta = get_distritos(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "nombre", "nombre_corto", "es_distrito_judicial")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
            registro["nombre_corto"],
            registro["es_distrito_judicial"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")
