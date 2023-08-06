from typing import Optional

import typer
from rich import print

app = typer.Typer()


@app.callback()
def callback():
    """Awesome Portal Gun"""


@app.command()
def shoot():
    """Shoot the portal gun"""
    typer.echo("Shooting portal gun")
    print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")


@app.command()
def load():
    """Load the portal gun"""
    typer.echo("Loading portal gun")


@app.command()
def say_hello(name: str, city: Optional[str] = None):
    """Типа говорит привет и приглашает попить кофе"""
    print(f"Hello {name}")
    if city:
        print(f"Let's have a coffee in {city}")


if __name__ == "__main__":
    app()
