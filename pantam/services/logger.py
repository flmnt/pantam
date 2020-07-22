from typing import Callable, Optional
from sys import stdout
from mypy_extensions import Arg
from colored import fg, attr

BANTAM: str = fg("yellow") + attr("bold") + "BANTAM: " + attr("reset")

WriteStream = Callable[[Arg(str, "s")], int]


class Logger:
    def __init__(self, write_stream: Optional[WriteStream] = None) -> None:
        if write_stream is None:
            self.write_stream = stdout.write
        else:
            self.write_stream = write_stream

    def __write(self, message: str) -> None:
        """Write message to stdout."""
        self.write_stream(str(BANTAM + message) + "\n")

    def info(self, message: str) -> None:
        """Print info message."""
        self.__write(fg("blue") + attr("bold") + message + attr("reset"))

    def success(self, message: str) -> None:
        """Print success message"""
        self.__write(fg("green") + attr("bold") + message + attr("reset"))

    def error(self, message: str) -> None:
        """Print error message"""
        self.__write(fg("red") + attr("bold") + message + attr("reset"))
