"""
CLI Typer
"""
import typer

from cit_citas.main import app as cit_citas_app  # pylint: disable=import-error
from cit_clientes.main import app as cit_clientes_app  # pylint: disable=import-error
from cit_clientes_registros.main import app as cit_clientes_registros_app  # pylint: disable=import-error

app = typer.Typer()
app.add_typer(cit_citas_app, name="citas")
app.add_typer(cit_clientes_app, name="clientes")
app.add_typer(cit_clientes_registros_app, name="registros")

if __name__ == "__main__":
    app()
