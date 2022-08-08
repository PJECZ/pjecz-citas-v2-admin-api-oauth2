"""
Cit Servicios Typer Commands
"""
import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_cit_servicios

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
):
    """Consultar servicios"""
    rich.print("Consultar servicios...")
    try:
        respuesta = get_cit_servicios(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "clave", "descripcion", "duracion")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["descripcion"],
            registro["duracion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] servicios")
