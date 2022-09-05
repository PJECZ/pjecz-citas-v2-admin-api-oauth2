"""
Cit Citas - App
"""
import rich
import typer

from config.settings import LIMIT

app = typer.Typer()


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


@app.command()
def mostrar_agendadas_por_oficina_servicio(
    inicio: str = None,
    inicio_desde: str = None,
    inicio_hasta: str = None,
):
    """Mostrar cantidades de citas agendadas por oficina y servicio"""
    rich.print("Mostrar cantidades de citas agendadas por oficina y servicio...")


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
