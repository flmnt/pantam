import logging
from os import environ
from colored import fg, attr

logging.basicConfig(level=environ.get("PANTAM_LOG_LEVEL", "INFO"))

PANTAM: str = fg("yellow") + attr("bold") + "PANTAM: " + attr("reset")


class Logger:
    def __init__(self) -> None:
        self.info_logger = logging.getLogger("pantam.info")
        self.success_logger = logging.getLogger("pantam.success")
        self.error_logger = logging.getLogger("pantam.error")

    def info(self, message: str) -> None:
        """Print info message."""
        self.info_logger(PANTAM + fg("blue") + attr("bold") + message + attr("reset"))

    def success(self, message: str) -> None:
        """Print success message"""
        self.success_logger(
            PANTAM + fg("green") + attr("bold") + message + attr("reset")
        )

    def error(self, message: str) -> None:
        """Print error message"""
        self.error_logger(PANTAM + fg("red") + attr("bold") + message + attr("reset"))
