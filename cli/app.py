#!/usr/bin/env python3
"""
CLI Typer main application
"""
import typer

from commands.cit_citas.commands import app as cit_citas_app
from commands.cit_clientes.commands import app as cit_clientes_app
from commands.cit_clientes_recuperaciones.commands import app as cit_clientes_recuperaciones_app

app = typer.Typer()
app.add_typer(cit_citas_app, name="cit_citas")
app.add_typer(cit_clientes_app, name="cit_clientes")
app.add_typer(cit_clientes_recuperaciones_app, name="cit_clientes_recuperaciones")

if __name__ == "__main__":
    app()
