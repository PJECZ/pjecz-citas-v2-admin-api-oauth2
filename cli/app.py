#!/usr/bin/env python3
"""
CLI Typer main application
"""
import typer

from commands.cit_categorias.app import app as cit_categorias_app
from commands.cit_citas.app import app as cit_citas_app
from commands.cit_clientes.app import app as cit_clientes_app
from commands.cit_clientes_recuperaciones.app import app as cit_clientes_recuperaciones_app
from commands.cit_clientes_registros.app import app as cit_clientes_registros_app
from commands.cit_dias_disponibles.app import app as cit_dias_disponibles_app
from commands.cit_servicios.app import app as cit_servicios_app
from commands.distritos.app import app as distritos_app
from commands.materias.app import app as materias_app
from commands.oficinas.app import app as oficinas_app
from commands.roles.app import app as roles_app
from commands.usuarios.app import app as usuarios_app

app = typer.Typer()
app.add_typer(cit_categorias_app, name="cit_categorias")
app.add_typer(cit_citas_app, name="cit_citas")
app.add_typer(cit_clientes_app, name="cit_clientes")
app.add_typer(cit_clientes_recuperaciones_app, name="cit_clientes_recuperaciones")
app.add_typer(cit_clientes_registros_app, name="cit_clientes_registros")
app.add_typer(cit_dias_disponibles_app, name="cit_dias_disponibles")
app.add_typer(cit_servicios_app, name="cit_servicios")
app.add_typer(distritos_app, name="distritos")
app.add_typer(materias_app, name="materias")
app.add_typer(oficinas_app, name="oficinas")
app.add_typer(roles_app, name="roles")
app.add_typer(usuarios_app, name="usuarios")

if __name__ == "__main__":
    app()
