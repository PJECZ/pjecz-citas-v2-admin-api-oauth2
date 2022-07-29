"""
CLI Cit Clientes
"""
import requests
import typer
import rich

import autentificar

app = typer.Typer()


def get_cit_clientes(base_url: str, authorization_header: dict) -> dict:
    """Consultar citas"""
    parametros = {"limit": 10}
    try:
        response = requests.get(
            f"{base_url}/cit_clientes",
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
def ver():
    """Ver"""
    print("Ver")
    rich.print(
        get_cit_clientes(
            base_url=autentificar.base_url(),
            authorization_header=autentificar.autentificar(),
        )
    )


if __name__ == "__main__":
    app()
