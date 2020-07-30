#!/usr/bin/env python3

import typer
from cli.action import run_action
from cli.init import run_init
from cli.serve import run_serve


run = typer.Typer()


@run.command()
def init():
    """Configure a Pantam application"""
    run_init()


@run.command()
def action(file: str):
    """Create a new action route"""
    run_action(file)


@run.command()
def serve(dev: bool = False):
    """Create a new action route"""
    run_serve(dev)


if __name__ == "__main__":
    run()
