"""
CLI Cit Clientes
"""
import typer

app = typer.Typer()


@app.command()
def consultar():
    """Consultar"""
    print("Consultar clientes")


if __name__ == "__main__":
    app()
