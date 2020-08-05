#!/usr/bin/env python3

from typing import Any, List, Union
from os import getcwd, path
from pathlib import Path
from re import sub
from prompt_toolkit import prompt
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

def create_prompt(question: str, default: Union[str, bool]) -> Any:
    """Create an interactive prompt"""
    is_confirm = isinstance(default, bool)
    if is_confirm:
        default = "Y/n" if default else "y/N"
    answer = prompt("%s (%s) " % (question, default))
    if not answer and is_confirm:
        not_yes_no = r"[^YN]"
        answer = sub(not_yes_no, "", default)
    if not answer:
        answer = default
    if is_confirm:
        return answer in ["Y", "y"]
    return answer

def init() -> None:
    """Setup Pantam project"""
    clear()

    write_msg(welcome_msg())

    folder_name = path.basename(getcwd())

    index_file = create_prompt(name_index_file_msg(), "%s.py" % folder_name)
    actions_folder = create_prompt(name_actions_folder_msg(), "actions")
    do_create_action_files = create_prompt(create_actions_file_msg(False), True)

    action_files: List[str] = []

    while do_create_action_files:
        actions_file = create_prompt(
            name_actions_file_msg(),
            "index.py" if len(action_files) == 0 else ""
        )
        if actions_file not in action_files:
            action_files.append(actions_file)
        do_create_action_files = create_prompt(
             create_actions_file_msg(True),
             False
         )

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

    confirm = create_prompt(
        confirm_structure_msg(structure),
        True
    )

    if not confirm:
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
