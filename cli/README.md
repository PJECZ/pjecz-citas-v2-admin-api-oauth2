# Command Line Interface

Debe tener un archivo `.env` con las variables de entorno.

    HOST=127.0.0.1
    PORT=8006
    USERNAME=guillermo.valdes@pjecz.gob.mx
    PASSWORD=Gato62Negro

E instalar manualmente estos paquetes python porque no se incluyen en `requirements.txt`

    pip install openpyxl pandas python-dotenv requests sendgrid typer

Pruebe con la ayuda inicial con este comando

    python cli/main.py --help
