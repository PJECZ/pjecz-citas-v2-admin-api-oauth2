# pjecz-citas-v2-admin-api-oauth2

API de Citas V2 para brindar informacion a otros sistemas.

## Mejores practicas

Usa las recomendaciones de [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/)

### Respuesta exitosa

Status code: **200**

Body que entrega un listado

    {
        "success": true,
        "message": "Success",
        "result": {
            "total": 2812,
            "items": [ { "id": 1, ... } ],
            "limit": 100,
            "offset": 0
        }
    }

Body que entrega un item

    {
        "success": true,
        "message": "Success",
        "id": 123,
        ...
    }

### Respuesta fallida: registro no encontrado

Status code: **200**

Body

    {
        "success": false,
        "message": "No employee found for ID 100"
    }

### Respuesta fallida: ruta incorrecta

Status code: **404**

## Configure Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Configuracion

Cree un archivo para las variables de entorno `.env`

    # Base de datos
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_NAME=pjecz_citas_v2
    DB_USER=adminpjeczcitasv2
    DB_PASS=****************

    # CORS Origins separados por comas
    ORIGINS=http://localhost:8006,http://localhost:3000,http://127.0.0.1:8006,http://127.0.0.1:3000

    # Limite de citas pendientes por cliente
    LIMITE_CITAS_PENDIENTES=30

    # Salt sirve para cifrar el ID con HashID, debe ser igual que en la app Flask
    SALT=************************

    # Santander Web Pay Plus
    WPP_COMMERCE_ID=XXXXXXXX
    WPP_COMPANY_ID=XXXX
    WPP_BRANCH_ID=NNNN
    WPP_KEY=XXXXXXXX
    WPP_PASS=XXXXXXXX
    WPP_TIMEOUT=12
    WPP_URL=https://noexiste.com
    WPP_USER=XXXXXXXX

    # Timezone
    TZ=America/Mexico_City

    # URLs de las encuestas
    POLL_SYSTEM_URL=http://127.0.0.1:3000/poll_system
    POLL_SERVICE_URL=http://127.0.0.1:3000/poll_service

    # Arrancar con gunicorn o uvicorn
    ARRANCAR=uvicorn

Para Bash Shell cree un archivo `.bashrc` que se puede usar en el perfil de Konsole

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

    source .venv/bin/activate
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi

    figlet Citas V2 API Key
    echo

    echo "== Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   ARRANCAR: ${ARRANCAR}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_PORT: ${DB_PORT}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   LIMITE_CITAS_PENDIENTES: ${LIMITE_CITAS_PENDIENTES}"
    echo "   ORIGINS: ${ORIGINS}"
    echo "   SALT: ${SALT}"
    echo "   TZ: ${TZ}"
    echo "   WPP_COMMERCE_ID: ${WPP_COMMERCE_ID}"
    echo "   WPP_COMPANY_ID: ${WPP_COMPANY_ID}"
    echo "   WPP_BRANCH_ID: ${WPP_BRANCH_ID}"
    echo "   WPP_KEY: ${WPP_KEY}"
    echo "   WPP_PASS: ${WPP_PASS}"
    echo "   WPP_TIMEOUT: ${WPP_TIMEOUT}"
    echo "   WPP_URL: ${WPP_URL}"
    echo "   WPP_USER: ${WPP_USER}"
    echo

    export PGHOST=$DB_HOST
    export PGPORT=$DB_PORT
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS

    alias arrancar="python3 ${PWD}/arrancar.py"
    echo "== Arrancar FastAPI con arrancar.py"
    echo "   arrancar"
    echo

## Instalacion

En Fedora Linux agregue este software

    sudo dnf -y groupinstall "Development Tools"
    sudo dnf -y install glibc-langpack-en glibc-langpack-es
    sudo dnf -y install pipenv poetry python3-virtualenv
    sudo dnf -y install python3-devel python3-docs python3-idle
    sudo dnf -y install python3-ipython

Clone el repositorio `pjecz-citas-v2-admin-api-oauth2`

    cd ~/Documents/GitHub/PJECZ
    git clone https://github.com/PJECZ/pjecz-citas-v2-admin-api-oauth2.git
    cd pjecz-citas-v2-admin-api-oauth2

Instale el entorno virtual y los paquetes necesarios

    poetry install

## FastAPI

Ejecute el script `arrancar.py` que contiene el comando y parametros para arrancar el servicio

    ./arrancar.py

## Google Cloud deployment

Crear el archivo `requirements.txt`

    poetry export -f requirements.txt --output requirements.txt --without-hashes

Y subir a Google Cloud

    gcloud app deploy
