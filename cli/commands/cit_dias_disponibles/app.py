"""
Cit Dias Disponibles - App
"""
import rich
import typer

from config.settings import LIMIT

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
):
    """Consultar dias disponibles"""
    rich.print("Consultar dias disponibles...")


@app.command()
def proximo():
    """Consultar proximo dia hábil"""
    rich.print("Consultar proximo dia hábil...")
