# pjecz-citas-v2-admin-api-oauth2

API OAuth2 del Sistema de Citas V2 para brindar informacion a otros sistemas.

## Configure Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Configuracion

Cree el archivo `.env` con este contenido

    # Base de datos
    DB_HOST=127.0.0.1
    DB_NAME=pjecz_citas_v2
    DB_USER=adminpjeczcitasv2
    DB_PASS=****************

    # OAuth2, para SECRET_KEY use openssl rand -hex 24
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ALGORITHM=HS256
    SECRET_KEY=************************************************

    # Salt sirve para cifrar el ID con HashID, debe ser igual que en la app Flask
    SALT=************************

Cree el archivo `instance/settings.py` con este contenido

    """
    Configuración para desarrollo
    """
    import os

    # Variables de entorno
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_NAME = os.environ.get("DB_NAME", "pjecz_citas_v2")
    DB_PASS = os.environ.get("DB_PASS", "wrongpassword")
    DB_USER = os.environ.get("DB_USER", "nouser")

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

Cree un archivo `.bashrc` que le cargue las variables de entorno al abrir un perfil en Konsole

    #!/bin/bash

    echo "== Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   SALT: ${SALT}"
    echo "   SECRET_KEY: ${SECRET_KEY}"
    echo

    export PGHOST=$DB_HOST
    export PGPORT=5432
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS

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

Ejecute el script `arrancar.py` que contiene el comando y parametros para arrancar el servicio

    ./arrancar.py

O use el comando para arrancar con uvicorn

    uvicorn --host=127.0.0.1 --port 8006 --reload citas_admin.app:app

O use el comando para arrancar con gunicorn

    gunicorn --workers=2 --bind 127.0.0.1:8006 citas_admin.app:app

## Command Line Interface

Lea `cli/README.md` para saber como configurar el CLI

Ejecute el script `cli/app.py` para probar la API

    cli/app.py --help
