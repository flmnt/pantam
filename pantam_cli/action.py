#!/usr/bin/env python3

from os import getcwd
from pathlib import Path
import sys
from pantam_cli.utils.filesystem import (
    create_file,
    make_class_name,
    load_pantamrc_file,
)
from pantam_cli.utils.messages import (
    info_msg,
    error_msg,
    success_msg,
    write_error,
    write_msg,
    NewLine,
)
from pantam_cli.utils.templates import action_template
from pantam_cli.utils import clear


def action(action_file: str) -> None:
    """Create action file"""
    clear()

    options = load_pantamrc_file()

    try:
        actions_folder = options["actions_folder"]
        write_msg(info_msg("Creating %s/%s file..." % (actions_folder, action_file)))
        cwd = Path(getcwd())
        create_file(
            cwd / actions_folder / action_file,
            action_template(make_class_name(action_file)),
        )
        write_msg(
            success_msg(" Done!"), NewLine.after,
        )
    except FileExistsError:
        write_msg(
            error_msg(" file exists, skipping"), NewLine.after,
        )


def run_action(action_file: str) -> None:
    """CLI runner for action()"""
    try:
        action(action_file)
        write_msg(success_msg("Your new action `%s` is ready!" % action_file))
    except Exception as error:
        write_error(error_msg(str(error)))


if __name__ == "__main__":
    file_name = sys.argv[1]
    run_action(file_name)
