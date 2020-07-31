#!/usr/bin/env python3

import subprocess
import sys
from atexit import register
from pantam_cli.utils.filesystem import load_pantamrc_file
from pantam_cli.utils import clear

process = None


def run_serve() -> None:
    """Serve Pantam application"""
    clear()
    options = load_pantamrc_file()
    entrypoint = options["entrypoint"]
    argument = "python %s" % entrypoint
    process = subprocess.Popen(argument, shell=True)


def stop_serve() -> None:
    """Stop Pantam application"""
    process.kill()


if __name__ == "__main__":
    run_serve()
    register(stop_serve)
