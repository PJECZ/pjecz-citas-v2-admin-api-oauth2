"""
Usuarios Typer Commands
"""
import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_usuarios

app = typer.Typer()


@app.command()
def consultar(
    limit: int = 40,
    autoridad_id: int = None,
    oficina_id: int = None,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")
    try:
        respuesta = get_usuarios(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
            autoridad_id=autoridad_id,
            oficina_id=oficina_id,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Distrito", "Autoridad", "Oficina", "email", "Nombres", "A. Paterno", "A. Materno")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["distrito_nombre_corto"],
            registro["autoridad_descripcion_corta"],
            registro["oficina_clave"],
            registro["email"],
            registro["nombres"],
            registro["apellido_paterno"],
            registro["apellido_materno"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] usuarios")
