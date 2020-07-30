from typing import TypedDict, Union
from os import getcwd, mkdir
from json import dumps, loads
from pathlib import Path
import sys
from pantam_cli.utils.messages import error_msg, write_error


def create_file(file_path: Union[str, Path], data: str) -> None:
    """Create a file"""
    new_file = open(file_path, "w")
    new_file.write(data)
    new_file.close()


def create_folder(folder_path: str) -> None:
    """Create a folder"""
    mkdir(folder_path)


def make_class_name(file_name: str) -> str:
    """Format file name to class name"""
    return file_name.replace(r".py", "").replace("_", " ").title().replace(" ", "")


class CliOptions(TypedDict):
    actions_folder: str
    entrypoint: str
    dev_port: int
    port: int


def create_pantamrc_file(options: CliOptions) -> None:
    """Create pantamrc.json file"""
    create_file("./.pantamrc.json", dumps(options))


def load_pantamrc_file() -> CliOptions:
    """Load pantamrc.json file"""
    cwd = Path(getcwd())
    try:
        config = open(cwd / ".pantamrc.json", "r")
        options: CliOptions = loads(config.read())
        return options
    except:
        write_error(
            error_msg("Cannot find .pantamrc.json file. Trying running `pantam init`")
        )
        sys.exit(1)
