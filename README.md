# pjecz-citas-v2-admin-api-oauth2

API OAuth2 del Sistema de Citas V2 para brindar informacion a otros sistemas.

## Mejores practicas

Se va a mejorar con los consejos en [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/)

### Escenario exitoso

Status code: **200**

Body que entrega un listado

    {
        "success": true,
        "message": "Success",
        "result": {
            "total": 914,
            "items": [ { "id": 1 } ],
            "limit": 100,
            "offset": 0
        }
    }

### Escenario fallido: registro no encontrado

Status code: **200**

Body

    {
        "success": false,
        "message": "No employee found for ID 100"
    }

### Escenario fallido: ruta incorrecta

Status code: **404**

## Configure Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Configuracion

Genere el `SECRET_KEY`

    openssl rand -hex 32

Cree un archivo para las variables de entorno `.env`

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

Cree el archivo `instance/settings.py`

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

    # CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend
    # running in a browser has JavaScript code that communicates with a backend,
    # and the backend is in a different "origin" than the frontend.
    # https://fastapi.tiangolo.com/tutorial/cors/
    ORIGINS = [
        "http://localhost:8006",
        "http://localhost:3000",
        "http://127.0.0.1:8006",
        "http://127.0.0.1:3000",
    ]

Para Bash Shell cree un archivo `.bashrc` que se puede usar en el perfil de Konsole

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

    source .venv/bin/activate
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi

    figlet Citas V2 API OAuth2
    echo

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

    alias arrancar="uvicorn --port 8006 --reload citas_admin.app:app"
    echo "-- FastAPI"
    echo "   arrancar"
    echo

## Instalacion

Clone el repositorio `pjecz-citas-v2-admin-api-oauth2`

    cd ~/Documents/GitHub/PJECZ
    git clone https://github.com/PJECZ/pjecz-citas-v2-admin-api-oauth2.git
    cd pjecz-citas-v2-admin-api-oauth2

Instale el entorno virtual y los paquetes necesarios

    poetry install

## FastAPI

Ejecute el script `arrancar.py` que contiene el comando y parametros para arrancar el servicio

    ./arrancar.py

O use el comando para arrancar con uvicorn

    uvicorn --host=127.0.0.1 --port 8006 --reload citas_admin.app:app

O use el comando para arrancar con gunicorn

    gunicorn --workers=2 --bind 127.0.0.1:8006 citas_admin.app:app

## Command Line Interface

Lea `cli/README.md` para saber como configurar el CLI

Ejecute el script `cli/app.py`

    cli/app.py --help

## Google Cloud deployment

Crear el archivo `requirements.txt`

    poetry export -f requirements.txt --output requirements.txt --without-hashes

Y subir a Google Cloud

    gcloud app deploy
