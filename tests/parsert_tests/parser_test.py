from unittest import TestCase, main

from parser.parser import Parser
from parser.parse_errors import Parse_errors


class Parser_test(TestCase):
    def test_parsing_with_none(self):
        self.assertEqual(Parser.parsing(None), Parse_errors.NO_FILES)

    def test_parsing_with_one_arg(self):
        self.assertEqual(Parser.parsing(["abc"]), Parse_errors.NO_FILES)

    def test_parsing_with_min_correct_args(self):
        self.assertEqual(Parser.parsing(["abc", "qve"]), Parse_errors.OK)

    def test_paring_with_many_args(self):
        self.assertEqual(Parser.parsing(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
                         Parse_errors.OK)


class ParserConfig_test(TestCase):
    def test_config_file_with_none(self):
        self.assertEqual(Parser.check_config_file(None),
                         Parse_errors.NO_CONFIG)

    def test_incorrect_config_file(self):
        self.assertEqual(Parser.check_config_file("Abc.c"),
                         Parse_errors.NO_CONFIG)

    def test_correct_config_file(self):
        self.assertEqual(Parser.check_config_file("Config.yaml"),
                         Parse_errors.OK)


class File_extension_analyze_test(TestCase):

    def test_with_none(self):
        correct_files = []
        Parser.file_extension_analyze([], correct_files, [".c", ".h"])
        self.assertEqual(correct_files, [])

    def test_with_one_correct(self):
        correct_files = []
        Parser.file_extension_analyze(["abc", "c.c", "sajkskajska", "qsasa.s"],
                                      correct_files, [".c", ".h"])
        self.assertEqual(correct_files, ["c.c"])

    def test_with_all_correct_files(self):
        correct_files = []
        Parser.file_extension_analyze(
            ["abc.c", "c.c", "sajkskajska.c", "qsasa.c", "abc.h", "c.h",
             "sajkskajska.h", "qsasa.h"], correct_files,
            [".c", ".h"])
        self.assertEqual(len(correct_files), 8)


if __name__ == "__main__":
    main()
