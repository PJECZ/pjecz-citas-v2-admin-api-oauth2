"""
CLI Typer main application
"""
import typer

import cit_citas
import cit_clientes
import cit_clientes_recuperaciones

app = typer.Typer()
app.add_typer(cit_citas.app, name="cit_citas")
app.add_typer(cit_clientes.app, name="cit_clientes")
app.add_typer(cit_clientes_recuperaciones.app, name="cit_clientes_recuperaciones")

if __name__ == "__main__":
    app()
