"""
CLI Commands Distritos App
"""
import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
from lib.exceptions import CLIAnyError

from .request_api import get_distritos

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar distritos"""
    rich.print("Consultar distritos...")
    try:
        respuesta = get_distritos(
            authorization_header=authorization_header(),
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre", "Nombre Corto", "Es D.J.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
            registro["nombre_corto"],
            "SI" if registro["es_distrito_judicial"] else "NO",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas")
