"""Logger is a Pantam services module"""

from colored import fg, attr

BANTAM = fg("yellow") + attr("bold") + "BANTAM: " + attr("reset")


class Logger:
    """Logger writes info, success, and error messages to stdout"""

    def __init__(self, write_stream=None):
        self.write_stream = write_stream

    def __write(self, message):
        """Write message to stdout"""
        self.write_stream(BANTAM + message)

    def info(self, message):
        """Log out info message"""
        self.__write(fg("blue") + attr("bold") + message + attr("reset"))

    def success(self, message):
        """Log out success message"""
        self.__write(fg("green") + attr("bold") + message + attr("reset"))

    def error(self, message):
        """Log out error message"""
        self.__write(fg("red") + attr("bold") + message + attr("reset"))
