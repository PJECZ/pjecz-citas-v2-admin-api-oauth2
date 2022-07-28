"""
CLI Cit Clientes Registros
"""
import typer

app = typer.Typer()


@app.command()
def consultar():
    """Consultar"""
    print("Consultar regsitros de clientes")


if __name__ == "__main__":
    app()
