"""
Cit Clientes Registros - App
"""
import rich
import typer

from config.settings import LIMIT

app = typer.Typer()


@app.command()
def consultar(
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    limit: int = LIMIT,
    nombres: str = None,
    registrado: bool = False,
    offset: int = 0,
):
    """Consultar registros de los clientes"""
    rich.print("Consultar registros de los clientes...")


@app.command()
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de registros creados por dia"""
    rich.print("Mostrar cantidades de registros creados por dia...")
