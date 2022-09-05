"""
CLI Commands Cit Citas App
"""
from datetime import datetime

import pandas as pd
import rich
import typer

from config.settings import LIMIT
from lib.authentication import authorization_header
from lib.exceptions import CLIAnyError
from lib.formats import df_to_table

from .request_api import get_cit_citas, get_cit_citas_agendadas_por_oficina_servicio, get_cit_citas_creados_por_dia

app = typer.Typer()

# Pandas options on how to display dataframes
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 150)


@app.command()
def consultar(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    estado: str = None,
    inicio: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
):
    """Consultar citas"""
    rich.print("Consultar citas...")
    try:
        respuesta = get_cit_citas(
            authorization_header=authorization_header(),
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            cit_servicio_id=cit_servicio_id,
            cit_servicio_clave=cit_servicio_clave,
            estado=estado,
            inicio=inicio,
            limit=limit,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Oficina", "Inicio", "Nombre", "Servicio", "Estado")
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
    email: str,
    inicio: str,
    oficina_clave: str,
    limit: int = LIMIT,
):
    """Enviar mensaje con citas"""
    rich.print("Enviar mensaje con citas...")


@app.command()
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    distrito_id: int = None,
):
    """Mostrar cantidades de citas creadas por dia"""
    rich.print("Mostrar cantidades de citas creadas por dia...")

    # Solicitar datos
    try:
        respuesta = get_cit_citas_creados_por_dia(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar tabla en la terminal
    console = rich.console.Console()
    table = rich.table.Table()
    table.add_column("Creado")
    table.add_column("Cantidad", justify="right")
    for creado, cantidad in respuesta["items"].items():
        table.add_row(creado, str(cantidad))
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")


@app.command()
def mostrar_agendadas_por_oficina_servicio(
    inicio: str = None,
    inicio_desde: str = None,
    inicio_hasta: str = None,
):
    """Mostrar cantidades de citas agendadas por oficina y servicio"""
    rich.print("Mostrar cantidades de citas agendadas por oficina y servicio...")

    # Solicitar datos
    try:
        respuesta = get_cit_citas_agendadas_por_oficina_servicio(
            authorization_header=authorization_header(),
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Convertir datos a pandas dataframe
    df = pd.DataFrame(respuesta["items"])

    # Cambiar el tipo de columna a categoria
    df.oficina = df.oficina.astype("category")
    df.servicio = df.servicio.astype("category")

    # Crear una tabla pivote
    pivot_table = df.pivot_table(
        index="oficina",
        columns="servicio",
        values="cantidad",
        aggfunc="sum",
    )

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Oficinas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")


@app.command()
def enviar_informe_diario(
    email: str,
    test: bool = True,
):
    """Enviar informe diario"""
    rich.print("Enviar informe diario...")


@app.command()
def enviar_agenda_a_usuarios(
    limit: int = 200,
    test: bool = True,
):
    """Enviar la agenda de las citas a los usuarios"""
    rich.print("Enviar la agenda de las citas a los usuarios...")
