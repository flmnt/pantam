#!/usr/bin/env python3

import subprocess
from atexit import register
from pantam_cli.utils.filesystem import load_pantamrc_file
from pantam_cli.utils import clear


def run_serve() -> None:
    """Serve Pantam application"""
    clear()
    options = load_pantamrc_file()
    entrypoint = options["entrypoint"]
    argument = "python %s" % entrypoint
    process = subprocess.Popen(argument, shell=True)
    register(process.kill)


if __name__ == "__main__":
    run_serve()
