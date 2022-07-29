"""
CLI Cit Citas
"""
import requests
import typer
from rich.console import Console
from rich.table import Table

import api
import exceptions

app = typer.Typer()


def get_cit_citas(base_url: str, authorization_header: dict) -> dict:
    """Consultar citas"""
    parametros = {"limit": 10}
    try:
        response = requests.get(
            f"{base_url}/cit_citas",
            headers=authorization_header,
            params=parametros,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise ValueError("Error porque la respuesta de la API no es correcta")
    return data_json


@app.command()
def exportar():
    """Exportar"""
    print("Exportar")


@app.command()
def consultar():
    """Consultar"""
    print("Consultar las citas")
    try:
        respuesta = get_cit_citas(
            base_url=api.base_url(),
            authorization_header=api.authorization(),
        )
    except (exceptions.AuthenticationException, exceptions.ConfigurationException) as error:
        raise typer.Exit(code=1) from error
    console = Console()
    table = Table("id", "oficina", "inicio", "nombre", "servicio", "estado")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["oficina_clave"],
            registro["inicio"],
            registro["cit_cliente_nombre"],
            registro["cit_servicio_clave"],
            registro["estado"],
        )
    console.print(table)


if __name__ == "__main__":
    app()
