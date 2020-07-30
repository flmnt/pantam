# pylint: disable=missing-function-docstring
from unittest.mock import Mock
from colored import fg, attr
from pantam.services import Logger

PANTAM: str = fg("yellow") + attr("bold") + "PANTAM: " + attr("reset")


def test_logger_info_msg():
    mock = Mock()
    logger = Logger(mock)
    logger.info("test")
    mock.assert_called_once_with(
        PANTAM + fg("blue") + attr("bold") + "test" + attr("reset") + "\n"
    )


def test_logger_success_msg():
    mock = Mock()
    logger = Logger(mock)
    logger.success("test")
    mock.assert_called_once_with(
        PANTAM + fg("green") + attr("bold") + "test" + attr("reset") + "\n"
    )


def test_logger_error_msg():
    mock = Mock()
    logger = Logger(mock)
    logger.error("test")
    mock.assert_called_once_with(
        PANTAM + fg("red") + attr("bold") + "test" + attr("reset") + "\n"
    )
