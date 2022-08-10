"""
Cit Citas Commands
"""
from datetime import datetime
import locale
import os

from dotenv import load_dotenv
import pandas as pd
import rich
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from tabulate import tabulate
import typer

import lib.connections
import lib.exceptions

from .crud import get_cit_citas, get_cit_citas_cantidades_creados_por_dia, get_cit_citas_cantidades_agendadas_por_oficina_servicio

app = typer.Typer()

locale.setlocale(locale.LC_TIME, "es_MX.utf8")

# Pandas options on how to display dataframes
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 150)

# SendGrid environment variables
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")


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
    email: str,
    fecha: str,
    oficina_clave: str,
    estado: str = "PENDIENTE",
    limit: int = 400,
):
    """Enviar mensaje con citas"""
    rich.print("Enviar mensaje con citas...")
    # Validate sendgrid environment variables
    try:
        if SENDGRID_API_KEY is None or SENDGRID_API_KEY == "":
            raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_API_KEY")
        if SENDGRID_FROM_EMAIL is None or SENDGRID_FROM_EMAIL == "":
            raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    # Get data
    try:
        respuesta = get_cit_citas(
            base_url=lib.connections.base_url(),
            authorization_header=lib.connections.authorization(),
            limit=limit,
            fecha=fecha,
            oficina_clave=oficina_clave,
            estado=estado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    # Terminate if no data
    if respuesta["total"] == 0:
        typer.secho("No hay citas para enviar", fg=typer.colors.YELLOW)
        raise typer.Exit()
    # Convert data to HTML table
    headers = ["ID", "Hora", "Nombre", "Servicio", "Notas"]
    rows = []
    for item in respuesta["items"]:
        inicio = datetime.strptime(item["inicio"], "%Y-%m-%dT%H:%M:%S")
        rows.append(
            [
                item["id"],
                inicio.strftime("%H:%M"),
                item["cit_cliente_nombre"],
                item["cit_servicio_clave"],
                item["notas"],
            ]
        )
    table_html = tabulate(rows, headers=headers, tablefmt="html")
    # Apply style to table
    table_html = table_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    # Add padding to table
    table_html = table_html.replace('<td style="', '<td style="padding: 4px;')
    table_html = table_html.replace("<td>", '<td style="padding: 4px;">')
    # Create message
    subject = f"Citas de la oficina {oficina_clave} para la fecha {fecha}"
    elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    contenidos = []
    contenidos.append("<style> td {border:2px black solid !important} </style>")
    contenidos.append("<h1>PJECZ Citas V2</h1>")
    contenidos.append(f"<h2>{subject}</h2>")
    contenidos.append(table_html)
    contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
    contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")
    # Send message
    sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(SENDGRID_FROM_EMAIL)
    to_email = To(email)
    content = Content("text/html", "<br>".join(contenidos))
    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )
    sendgrid_client.client.mail.send.post(request_body=mail.get())
    # Print message
    rich.print(f"Mensaje enviado a [blue]{email}[/blue] con [green]{respuesta['total']}[/green] citas")


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
def enviar_cantidades_creados_por_dia(
    email: str,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Enviar cantidades de citas creadas por dia"""
    rich.print("Enviar cantidades de citas creadas por dia...")
    # Validate sendgrid environment variables
    try:
        if SENDGRID_API_KEY is None or SENDGRID_API_KEY == "":
            raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_API_KEY")
        if SENDGRID_FROM_EMAIL is None or SENDGRID_FROM_EMAIL == "":
            raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    # Get data
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
    # Terminate if no data
    if respuesta["total"] == 0:
        typer.secho("No hay datos con las fechas dadas", fg=typer.colors.YELLOW)
        raise typer.Exit()


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


@app.command()
def enviar_cantidades_agendadas_por_oficina_servicio(
    email: str,
    inicio: str = None,
    inicio_desde: str = None,
    inicio_hasta: str = None,
):
    """Enviar cantidades de citas agendadas por oficina y servicio"""
    rich.print("Enviar cantidades de citas agendadas por oficina y servicio...")
    # Validate sendgrid environment variables
    try:
        if SENDGRID_API_KEY is None or SENDGRID_API_KEY == "":
            raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_API_KEY")
        if SENDGRID_FROM_EMAIL is None or SENDGRID_FROM_EMAIL == "":
            raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    # Get data
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
    # Terminate if no data
    if respuesta["total"] == 0:
        typer.secho("No hay datos con las fechas dadas", fg=typer.colors.YELLOW)
        raise typer.Exit()
