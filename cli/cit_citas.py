"""
CLI Cit Citas
"""
import typer

app = typer.Typer()


@app.command()
def consultar():
    """Consultar"""
    print("Consultar citas")


if __name__ == "__main__":
    app()
