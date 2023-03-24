from config_reader.config_reader import Config_reader
from parser.parser import Parser
from parser.parse_errors import Parse_errors
import sys
from argparse import ArgumentParser


def main():
    parser_cli = ArgumentParser(description="Simple linter for C language")
    parser_cli.add_argument("-config", help="config for lint", type=str)
    parser_cli.add_argument("-files", help="files", type=str, nargs='*')
    args = parser_cli.parse_args()
    parser_files = Parser()
    print(args.files)
    if parser_files.check_config_file(args.config) == Parse_errors.NO_CONFIG:
        print(Parse_errors.NO_CONFIG.value)
        return

    correct_files = list()
    config = Config_reader(args.config)
    code = parser_files.file_extension_analyze(args.files, correct_files, config)
    if code == Parse_errors.NO_EXTENSION_FILES:
        print(code.value)
        return


if __name__ == "__main__":
    main()
