from unittest import TestCase

from tests.parsert_tests.linter_tests import Checkers_test, Checkers_lint
from tests.parsert_tests.parser_test import Parser_test, \
    File_extension_analyze_test


class TestMain(TestCase):
    Checkers_test()
    Checkers_lint()
    Parser_test()
    File_extension_analyze_test()
