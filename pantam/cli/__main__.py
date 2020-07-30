#!/usr/bin/env python3

import typer

app = typer.Typer()

# this is a temporary example file


@app.command()
def hello(name: str):
    """Say hello"""
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    """Say goodbye"""
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
