"""
CLI Typer
"""
import typer

import cit_citas  # pylint: disable=import-error
import cit_clientes  # pylint: disable=import-error
import cit_clientes_registros  # pylint: disable=import-error

app = typer.Typer()
app.add_typer(cit_citas.app, name="citas")
app.add_typer(cit_clientes.app, name="clientes")
app.add_typer(cit_clientes_registros.app, name="registros")

if __name__ == "__main__":
    app()
