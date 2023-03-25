import pytest
import coverage

from parser.parser import Parser
from parser.parse_errors import Parse_errors


def test_parsing_with_none():
    assert Parser.parsing(None) == Parse_errors.NO_FILES


def test_parsing_with_one_arg():
    assert Parser.parsing(["abc", "qve"]) == Parse_errors.OK


def test_paring_with_many_args():
    assert Parser.parsing(
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]) == Parse_errors.OK


def test_config_file_with_none():
    assert Parser.check_config_file(None) == Parse_errors.NO_CONFIG


def test_incorrect_config_file():
    assert Parser.check_config_file("Abc.c") == Parse_errors.NO_CONFIG


def test_correct_config_file():
    assert Parser.check_config_file("Config.yaml") == Parse_errors.OK


def test_with_none():
    correct_files = []
    Parser.file_extension_analyze([], correct_files, [".c", ".h"])
    assert correct_files == []


def test_with_one_correct():
    correct_files = []
    Parser.file_extension_analyze(["abc", "c.c", "sajkskajska", "qsasa.s"],
                                  correct_files, [".c", ".h"])
    assert correct_files == ["c.c"]


def test_with_all_correct_files():
    correct_files = []
    Parser.file_extension_analyze(
        ["abc.c", "c.c", "sajkskajska.c", "qsasa.c", "abc.h", "c.h",
         "sajkskajska.h", "qsasa.h"], correct_files,
        [".c", ".h"])
    assert len(correct_files) == 8
