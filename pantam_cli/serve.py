#!/usr/bin/env python3

from os import getenv
import sys
from uvicorn import run
from pantam_cli.utils.filesystem import load_pantamrc_file
from pantam_cli.utils import clear


def run_serve(dev_mode: bool) -> None:
    """Serve a Pantam application"""
    clear()
    options = load_pantamrc_file()
    entrypoint = options["entrypoint"].replace(".py", "")
    listen_port = (
        options["port"]
        if getenv("PANTAM_ENV", default="development") == "production"
        else options["dev_port"]
    )
    run("%s:app" % entrypoint, port=listen_port, reload=dev_mode)


if __name__ == "__main__":
    dev = sys.argv[1] if len(sys.argv) > 1 else ""
    run_serve(dev in ("--dev", "-d"))
