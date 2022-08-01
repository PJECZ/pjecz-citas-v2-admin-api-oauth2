# pjecz-citas-v2-admin-api-oauth2

API OAuth2 del Sistema de Citas V2 para brindar informacion a otros sistemas.

## Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Instalacion para desarrollo

Clone el repositorio `pjecz-citas-v2-admin-api-oauth2`

    cd ~/Documents/GitHub/PJECZ
    git clone https://github.com/PJECZ/pjecz-citas-v2-admin-api-oauth2.git
    cd pjecz-citas-v2-admin-api-oauth2

Instale el entorno virtual y los paquetes necesarios

    poetry install

Ingrese al entorno virtual con

    poetry shell

## Arrancar el servicio de la API en http://127.0.0.1:8006

Ejecute el script `arrancar.py`

    python arrancar.py

O use el comando para arrancar con uvicorn

    uvicorn --host=127.0.0.1 --port 8006 --reload citas_admin.app:app

O use el comando para arrancar con gunicorn

    gunicorn --workers=2 --bind 127.0.0.1:8006 citas_admin.app:app

## Command Line Interface

Para probar la API use el CLI

    python cli/app.py --help
