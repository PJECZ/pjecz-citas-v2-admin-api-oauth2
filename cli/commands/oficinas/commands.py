"""
Oficinas Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_oficinas

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    distrito_id: int = None,
    domicilio_id: int = None,
    puede_agendar_citas: bool = True,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")
    try:
        respuesta = get_oficinas(
            authorization_header=authorization_header(),
            limit=limit,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            puede_agendar_citas=puede_agendar_citas,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Distrito", "Descripcion", "P.A.C.", "Apertura", "Cierre", "L.P.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["descripcion_corta"],
            "SI" if bool(registro["puede_agendar_citas"]) else "",
            registro["apertura"],
            registro["cierre"],
            str(registro["limite_personas"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas")
