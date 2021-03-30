from logging import getLogger
from traceback import format_exc
from sys import stdout
from colored import fg, attr

PANTAM: str = fg("yellow") + attr("bold") + "PANTAM: " + attr("reset")
BREAK: str = "\n"


def write(colour: str, msg: str) -> None:
    """Format and print message to stdout"""
    stdout.write(PANTAM + fg(colour) + attr("bold") + msg + attr("reset") + BREAK)


class Logger:
    def __init__(self, debug=False) -> None:
        self.logger = getLogger("pantam")
        self.debug = debug

    def info(self, message: str) -> None:
        """Print info message."""
        self.logger.info(message)
        write("blue", message)

    def success(self, message: str) -> None:
        """Print success message"""
        self.logger.info(message)
        write("green", message)

    def error(self, message: str) -> None:
        """Print error message"""
        if self.debug:
            format_exc()
        self.logger.error(message)
        write("red", message)
