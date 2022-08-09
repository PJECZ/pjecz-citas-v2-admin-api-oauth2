"""
Cit Citas Commands
"""
from datetime import datetime

import pandas as pd
import typer
import rich

import lib.connections
import lib.exceptions

from .crud import get_cit_citas, get_cit_citas_cantidades_creados_por_dia, get_cit_citas_cantidades_agendadas_por_oficina_servicio

app = typer.Typer()

# Pandas options on how to display dataframes
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 150)


@app.command()
def consultar(
    limit: int = 40,
    fecha: str = None,
    email: str = None,
    oficina_clave: str = None,
    estado: str = None,
):
    """Consultar citas"""
    rich.print("Consultar citas...")
    try:
        respuesta = get_cit_citas(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
            fecha=fecha,
            cit_cliente_email=email,
            oficina_clave=oficina_clave,
            estado=estado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("id", "creado", "oficina", "inicio", "nombre", "servicio", "estado")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["oficina_clave"],
            inicio.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_nombre"],
            registro["cit_servicio_clave"],
            registro["estado"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")


@app.command()
def enviar(
    limit: int = 40,
    fecha: str = None,
    email: str = None,
    oficina_clave: str = None,
):
    """Enviar mensaje con citas"""
    rich.print("Enviar mensaje con citas...")


@app.command()
def mostrar_cantidades_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de citas creadas por dia"""
    rich.print("Mostrar cantidades de citas creadas por dia...")
    try:
        respuesta = get_cit_citas_cantidades_creados_por_dia(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("creado", "cantidad")
    for registro in respuesta["items"]:
        table.add_row(
            registro["creado"],
            str(registro["cantidad"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")


@app.command()
def mostrar_cantidades_agendadas_por_oficina_servicio(
    inicio: str = None,
    inicio_desde: str = None,
    inicio_hasta: str = None,
):
    """Mostrar cantidades de citas agendadas por oficina y servicio"""
    rich.print("Mostrar cantidades de citas agendadas por oficina y servicio...")
    try:
        respuesta = get_cit_citas_cantidades_agendadas_por_oficina_servicio(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    # Convert items to pandas dataframe
    df = pd.DataFrame(respuesta["items"])
    # Change type of columns oficina and servicio to category
    df.oficina = df.oficina.astype("category")
    df.servicio = df.servicio.astype("category")
    # Create a pivot table
    pivot_table = df.pivot_table(
        index="oficina",
        columns="servicio",
        values="cantidad",
        aggfunc="sum",
    )
    # Print the pivot table
    console = rich.console.Console()
    console.print(pivot_table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")
