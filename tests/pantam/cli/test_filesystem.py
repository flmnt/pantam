# pylint: disable=missing-function-docstring

from pantam.cli.utils.filesystem import create_file, make_class_name


def test_make_class_name():
    assert make_class_name("this_example.py") == "ThisExample"
