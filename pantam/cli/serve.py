import subprocess
import sys
from pantam.cli.utils.filesystem import load_pantamrc_file
from pantam.cli.utils import clear


def run_serve(dev_mode: bool) -> None:
    """Serve Pantam application"""
    clear()

    options = load_pantamrc_file()

    entrypoint = options["entrypoint"].replace(".py", "")
    port = options["dev_port"] if dev_mode else options["port"]

    argument = "uvicorn %s:app --port %s" % (entrypoint, port)

    if dev_mode:
        argument += " --reload"

    subprocess.Popen(argument, shell=True)


if __name__ == "__main__":
    dev = sys.argv[1] if len(sys.argv) > 1 else ""
    run_serve(dev in ("--dev", "-d"))
