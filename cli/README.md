# Command Line Interface

Debe tener un archivo `.env` con las variables de entorno.

    HOST=http://127.0.0.1:8006
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=C0nTr45en4

E instalar manualmente estos paquetes python porque no se incluyen en `requirements.txt`

    pip install openpyxl pandas python-dotenv requests sendgrid typer

Pruebe con la ayuda inicial con este comando

    python cli/main.py --help
