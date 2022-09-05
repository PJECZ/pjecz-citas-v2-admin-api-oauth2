"""
CLI Commands Cit Clientes Recuperaciones App
"""
import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
from lib.exceptions import CLIAnyError

app = typer.Typer()


@app.command()
def consultar(
    email: str = None,
    limit: int = LIMIT,
    recuperado: bool = False,
    offset: int = 0,
):
    """Consultar recuperaciones de los clientes"""
    rich.print("Consultar recuperaciones de los clientes...")


@app.command()
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de recuperaciones creadas por dia"""
    rich.print("Mostrar cantidades de recuperaciones creadas por dia...")


@app.command()
def reenviar(
    test: bool = True,
):
    """Reenviar mensajes de las recuperaciones de los clientes"""
    rich.print("Reenviar mensajes de las recuperaciones de los clientes...")
