"""
Distritos - App
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
    """Consultar distritos"""
    rich.print("Consultar distritos...")
