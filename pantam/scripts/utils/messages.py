from sys import stderr, stdout
from enum import Enum
from colored import fg, attr

PANTAM: str = fg("yellow") + attr("bold") + "PANTAM" + attr("reset")

colour_msg = lambda msg, colour: fg(colour) + attr("bold") + msg + attr("reset")
info_msg = lambda msg: colour_msg(msg, "blue")
success_msg = lambda msg: colour_msg(msg, "green")
error_msg = lambda msg: colour_msg(msg, "red")


class NewLine(Enum):
    before = 1
    after = 2
    both = 3


def write_msg(msg: str, spacing: NewLine = None) -> None:
    """Write message to stdout"""
    prefix: str = "\n" if spacing in (NewLine.before, NewLine.both) else ""
    suffix: str = "\n" if spacing in (NewLine.after, NewLine.both) else ""
    stdout.write("%s%s%s" % (prefix, msg, suffix))


def write_error(msg: str) -> None:
    """Write message to stderr"""
    stderr.write("\n%s\n" % msg)


welcome_msg = (
    lambda: PANTAM
    + """

The microframework for microservices.

Let's build your app...

"""
)

name_index_file_msg = lambda: "What is the name of your main script?"

name_actions_folder_msg = lambda: "What is the name of your actions folder?"


def create_actions_file_msg(second_run: bool):
    """Actions File Message"""
    article = "another" if second_run else "an"
    return "Do you want to create %s action file?" % article


name_actions_file_msg = lambda: "What is the name of your actions file?"

confirm_structure_msg = (
    lambda structure: """Your application will look like this:
%s

Happy to proceed?"""
    % structure
)
