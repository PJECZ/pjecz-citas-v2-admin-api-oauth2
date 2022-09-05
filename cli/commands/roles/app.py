"""
Roles - App
"""
import rich
import typer

from config.settings import LIMIT

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar roles"""
    rich.print("Consultar roles...")
