"""
CLI Autentificar
"""
import os

from dotenv import load_dotenv
import requests

load_dotenv()
HOST = os.getenv("HOST", "http://127.0.0.1:8006")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")


def autentificar() -> dict:
    """Autentificarse"""
    if HOST == "":
        raise Exception("No se ha definido el host")
    if USERNAME == "":
        raise Exception("No se ha definido el usuario")
    if PASSWORD == "":
        raise Exception("No se ha definido la contraseña")
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{HOST}/token", data=data, headers=headers)
    if response.status_code != 200:
        raise requests.HTTPError(response.text)
    token = response.json()["access_token"]
    authorization_header = {"Authorization": "Bearer " + token}
    return authorization_header


def base_url() -> str:
    """URL base de la API"""
    return f"{HOST}/v2"
