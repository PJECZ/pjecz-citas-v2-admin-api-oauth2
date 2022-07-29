"""
CLI Typer
"""
import typer

import cit_citas
import cit_clientes

app = typer.Typer()
app.add_typer(cit_citas.app, name="cit_citas")
app.add_typer(cit_clientes.app, name="cit_clientes")

if __name__ == "__main__":
    app()
