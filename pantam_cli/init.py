#!/usr/bin/env python3

from typing import List
from os import getcwd, path
from pathlib import Path
from PyInquirer import prompt
from pantam_cli.utils.filesystem import (
    create_file,
    create_folder,
    make_class_name,
    create_pantamrc_file,
)
from pantam_cli.utils.messages import (
    info_msg,
    error_msg,
    success_msg,
    write_error,
    write_msg,
    NewLine,
    welcome_msg,
    name_index_file_msg,
    name_actions_folder_msg,
    name_actions_file_msg,
    create_actions_file_msg,
    confirm_structure_msg,
)
from pantam_cli.utils.templates import action_template, index_template
from pantam_cli.utils.errors import CancelError
from pantam_cli.utils import clear


def init() -> None:
    """Setup Pantam project"""
    clear()

    write_msg(welcome_msg())

    folder_name = path.basename(getcwd())

    answers = prompt(
        [
            {
                "type": "input",
                "name": "index_file",
                "message": name_index_file_msg(),
                "default": "%s.py" % folder_name,
            },
            {
                "type": "input",
                "name": "actions_folder",
                "message": name_actions_folder_msg(),
                "default": "actions",
            },
            {
                "type": "confirm",
                "name": "create_actions_file",
                "message": create_actions_file_msg(False),
                "default": True,
            },
        ]
    )

    index_file = answers["index_file"]
    actions_folder = answers["actions_folder"]
    do_create_action_files = answers["create_actions_file"]

    action_files: List[str] = []

    while do_create_action_files:
        answers = prompt(
            [
                {
                    "type": "input",
                    "name": "actions_file",
                    "message": name_actions_file_msg(),
                    "default": "index.py" if len(action_files) == 0 else "",
                },
                {
                    "type": "confirm",
                    "name": "create_actions_file",
                    "message": create_actions_file_msg(True),
                    "default": False,
                },
            ]
        )
        if answers["actions_file"] not in action_files:
            action_files.append(answers["actions_file"])
        do_create_action_files = answers["create_actions_file"]

    action_files_map = list(map(lambda file_name: "|  |  %s" % file_name, action_files))
    action_files_flat = "\n".join(action_files_map)

    structure = """
| {index_file}
| {actions_folder}
{actions_files}""".format(
        index_file=index_file,
        actions_folder=actions_folder,
        actions_files=action_files_flat,
    )

    answers = prompt(
        [
            {
                "type": "confirm",
                "name": "confirm",
                "message": confirm_structure_msg(structure),
                "default": True,
            },
        ]
    )

    if not answers["confirm"]:
        raise CancelError("Cancelled!")

    write_msg(
        info_msg("Building your app! 🚀"), NewLine.both,
    )

    try:
        write_msg(info_msg("Creating %s file..." % index_file),)
        create_file(index_file, index_template())
        create_file("__init__.py", "")
        write_msg(success_msg(" done!"), NewLine.after)
    except FileExistsError:
        write_msg(error_msg(" file exists, skipping"), NewLine.after)

    try:
        write_msg(info_msg("Creating %s folder..." % actions_folder))
        create_folder(actions_folder)
        file_path = Path(getcwd())
        create_file(file_path / actions_folder / "__init__.py", "")
        write_msg(success_msg(" done!"), NewLine.after)
    except:
        write_msg(error_msg(" folder exists, skipping"), NewLine.after)

    for action_file in action_files:
        try:
            write_msg(
                info_msg("Creating %s/%s file..." % (actions_folder, action_file))
            )
            file_path = Path(getcwd())
            create_file(
                file_path / actions_folder / action_file,
                action_template(make_class_name(action_file)),
            )
            write_msg(success_msg(" done!"), NewLine.after)
        except:
            write_msg(error_msg(" file exists, skipping"), NewLine.after)

    try:
        write_msg(info_msg("Creating .pantamrc.json file..."))
        create_pantamrc_file(
            {
                "actions_folder": actions_folder,
                "entrypoint": index_file,
                "port": 5000,
                "dev_port": 5000,
            }
        )
        write_msg(success_msg(" done!"), NewLine.after)
    except:
        write_msg(error_msg(" file exists, skipping"), NewLine.after)


def run_init() -> None:
    """CLI runner for init()"""
    try:
        init()
        write_msg(
            success_msg("Your application is ready!"), NewLine.both,
        )
        write_msg(
            "Run " + success_msg("pantam serve") + " to begin...\n", NewLine.both,
        )
    except CancelError:
        write_error(error_msg("Setup cancelled..."))
    except Exception as error:
        write_error(error_msg(str(error)))


if __name__ == "__main__":
    run_init()
