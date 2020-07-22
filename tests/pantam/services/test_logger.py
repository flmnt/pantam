# pylint: disable=missing-function-docstring
from colored import fg, attr
from pantam.services import Logger

BANTAM: str = fg("yellow") + attr("bold") + "BANTAM: " + attr("reset")


def test_logger_info_msg(mocker):
    stub = mocker.stub(name="write_stream_stub")
    logger = Logger(stub)
    logger.info("test")
    stub.assert_called_once_with(
        BANTAM + fg("blue") + attr("bold") + "test" + attr("reset") + "\n"
    )


def test_logger_success_msg(mocker):
    stub = mocker.stub(name="write_stream_stub")
    logger = Logger(stub)
    logger.success("test")
    stub.assert_called_once_with(
        BANTAM + fg("green") + attr("bold") + "test" + attr("reset") + "\n"
    )


def test_logger_error_msg(mocker):
    stub = mocker.stub(name="write_stream_stub")
    logger = Logger(stub)
    logger.error("test")
    stub.assert_called_once_with(
        BANTAM + fg("red") + attr("bold") + "test" + attr("reset") + "\n"
    )
