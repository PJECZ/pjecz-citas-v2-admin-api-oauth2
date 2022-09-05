"""
Usuarios - App
"""
import rich
import typer

from config.settings import LIMIT

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")
