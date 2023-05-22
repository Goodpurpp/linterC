import unittest
from unittest import TestCase, main
from parameterized import parameterized, parameterized_class
from config_reader.config_reader import ConfigReader
from linter.checkers import is_empty_line, double_space, ops_before_space
from language.clang_tokens import ClangTokens
from linter.linter import _count_args, Linter


class Checkers_test(TestCase):
    def test_with_empty_token(self):
        self.assertEqual(is_empty_line([None, ClangTokens.EMPTY_LINE, None]),
                         True)

    def test_with_non_empty_token(self):
        self.assertEqual(is_empty_line([None, ClangTokens.OP, None]),
                         False)


@parameterized_class(("first_token", "second_token", "expectation"), [
    ([(0, 0), ClangTokens.SPACE, None],
     [(0, 0), ClangTokens.SPACE, None], True),
    ([(0, 0), ClangTokens.SPACE, None],
     [(1, 0), ClangTokens.SPACE, None], False)
])
class TestDoubleSpace(unittest.TestCase):
    def test_double_space(self):
        self.assertEqual(double_space(self.first_token, self.second_token),
                         self.expectation)


@parameterized_class(("first_token", "second_token", "expectation"), [
    ([(1, 1), ClangTokens.OP, ">"],
     [(1, 9), ClangTokens.SPACE, " "],
     False),
    ([(7, 17), ClangTokens.SPACE, " "],
     [(7, 18), ClangTokens.VAR, "0"],
     False),
    ([(7, 18), ClangTokens.VAR, "0"],
     [(7, 19), ClangTokens.OP, ";"],
     False),
    ([(7, 18), ClangTokens.VAR, "0"],
     [(8, 19), ClangTokens.OP, ";"],
     False),
])
class TestOps(unittest.TestCase):
    def test_ops_before_space(self):
        self.assertEqual(ops_before_space(self.first_token, self.second_token),
                         self.expectation)


class Checkers_lint(TestCase):
    def test_count_args(self):
        self.assertEqual(
            _count_args([(3, 6), ClangTokens.ARGS, "abc"],
                        [[(1, 1), ClangTokens.INCLUDE, "#include"],
                         [(1, 9), ClangTokens.SPACE, " "],
                         [(1, 10), ClangTokens.ARGS, "abc"],
                         [(2, 0), ClangTokens.EMPTY_LINE, "\\n"],
                         [(3, 1), ClangTokens.TYPE, "void"]]), 1)

    def test_tokenize(self):
        linter = Linter("config.yaml", "abc.c")
        self.assertEqual(linter._check_token("abc", [
            [(1, 1), ClangTokens.INCLUDE, "#include"],
            [(1, 9), ClangTokens.SPACE, " "],
            [(1, 10), ClangTokens.ARGS, "abc"],
            [(2, 0), ClangTokens.EMPTY_LINE, "\\n"],
            [(3, 1), ClangTokens.TYPE, "void"]]), ClangTokens.VAR)

    def test_init_conf(self):
        config_reader = ConfigReader("config.yaml")
        self.assertEqual(config_reader.max_line_len, 120)

    def test_token_with_op(self, _check_var_with_op=None):
        linter = Linter("config.yaml", "abc.c")
        self.assertEqual(
            linter._check_var_with_op([(12, 9), ClangTokens.OP, "("]),
            False)


if __name__ == "__main__":
    main()
