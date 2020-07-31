from typing import Callable, Optional
from sys import stdout
from colored import fg, attr

PANTAM: str = fg("yellow") + attr("bold") + "PANTAM: " + attr("reset")

WriteStream = Callable[[str], int]


class Logger:
    def __init__(self, write_stream: Optional[WriteStream] = None) -> None:
        if write_stream is None:
            self.write_stream = stdout.write
        else:
            self.write_stream = write_stream

    def __write(self, message: str) -> None:
        """Write message to stdout."""
        self.write_stream(str(PANTAM + message) + "\n")

    def info(self, message: str) -> None:
        """Print info message."""
        self.__write(fg("blue") + attr("bold") + message + attr("reset"))

    def success(self, message: str) -> None:
        """Print success message"""
        self.__write(fg("green") + attr("bold") + message + attr("reset"))

    def error(self, message: str) -> None:
        """Print error message"""
        self.__write(fg("red") + attr("bold") + message + attr("reset"))
