"""
Cit Servicios Typer Commands
"""
import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_cit_servicios

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar servicios"""
    rich.print("Consultar servicios...")
    try:
        respuesta = get_cit_servicios(
            authorization_header=authorization_header(),
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Descripcion", "Duracion", "Desde", "Hasta", "Dias Habilitados")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["descripcion"],
            registro["duracion"],
            str(registro["desde"]) if registro["desde"] is not None else "",
            str(registro["hasta"]) if registro["hasta"] is not None else "",
            registro["dias_habilitados"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] servicios")
