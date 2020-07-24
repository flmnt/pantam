# pylint: disable=missing-function-docstring
from unittest.mock import Mock
from colored import fg, attr
from pantam.services import Logger

BANTAM: str = fg("yellow") + attr("bold") + "BANTAM: " + attr("reset")


def test_logger_info_msg():
    mock = Mock()
    logger = Logger(mock)
    logger.info("test")
    mock.assert_called_once_with(
        BANTAM + fg("blue") + attr("bold") + "test" + attr("reset") + "\n"
    )


def test_logger_success_msg():
    mock = Mock()
    logger = Logger(mock)
    logger.success("test")
    mock.assert_called_once_with(
        BANTAM + fg("green") + attr("bold") + "test" + attr("reset") + "\n"
    )


def test_logger_error_msg():
    mock = Mock()
    logger = Logger(mock)
    logger.error("test")
    mock.assert_called_once_with(
        BANTAM + fg("red") + attr("bold") + "test" + attr("reset") + "\n"
    )
