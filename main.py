import typer
from typing import Optional
from pathlib import Path

app = typer.Typer(
    name="scripts",
    help="Una aplicación CLI potente con interfaz gráfica opcional",
    add_completion=False
)


@app.command()
def hello(
    name: str = typer.Argument(..., help="Tu nombre"),
    greeting: Optional[str] = typer.Option("Hola", "--greeting", "-g", help="Saludo personalizado")
):
    """
    Saluda a una persona con un mensaje personalizado.
    """
    typer.echo(f"{greeting}, {name}! 👋")


@app.command()
def info():
    """
    Muestra información sobre la aplicación.
    """
    typer.echo("🚀 Scripts CLI v0.1.0")
    typer.echo("Una aplicación CLI desarrollada con Typer")
    typer.echo("Incluye interfaz gráfica opcional con tkinter")


@app.command()
def gui():
    """
    Lanza la interfaz gráfica de la aplicación.
    """
    try:
        from gui import launch_gui
        launch_gui()
    except ImportError:
        typer.echo("❌ Error: El módulo GUI no está disponible", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
