"""
CLI Cit Citas
"""
import typer

app = typer.Typer()


@app.command()
def exportar():
    """Exportar"""
    print("Exportar")


@app.command()
def ver():
    """Ver"""
    print("Ver")


if __name__ == "__main__":
    app()
