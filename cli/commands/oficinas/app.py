"""
Oficinas - App
"""
import rich
import typer

from config.settings import LIMIT

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    domicilio_id: int = None,
    limit: int = LIMIT,
    puede_agendar_citas: bool = True,
    offset: int = 0,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")
