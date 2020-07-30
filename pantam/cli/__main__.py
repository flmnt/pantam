#!/usr/bin/env python3

import typer
from pantam.cli.action import run_action
from pantam.cli.init import run_init
from pantam.cli.serve import run_serve


cli = typer.Typer()


@cli.command()
def init():
    """Configure a Pantam application"""
    run_init()


@cli.command()
def action(file: str):
    """Create a new action route"""
    run_action(file)


@cli.command()
def serve(dev: bool = False):
    """Create a new action route"""
    run_serve(dev)


if __name__ == "__main__":
    cli()
