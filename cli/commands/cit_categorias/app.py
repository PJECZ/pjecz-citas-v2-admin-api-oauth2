"""
CLI Commands Cit Categorias App
"""
import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
from lib.exceptions import CLIAnyError

from .request_api import get_cit_categorias

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar categorias"""
    rich.print("Consultar categorias...")
    try:
        respuesta = get_cit_categorias(
            authorization_header=authorization_header(),
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] categorias")
