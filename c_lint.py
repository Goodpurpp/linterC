from config_reader.config_reader import Config_reader
from linter.linter import Linter
from parser.parser import Parser
from parser.parse_errors import Parse_errors
from parser.cli_parse import cli_parse


def main():
    args = cli_parse()
    parser_files = Parser()
    if parser_files.check_config_file(args.config) == Parse_errors.NO_CONFIG:
        print(Parse_errors.NO_CONFIG.value)
        return

    correct_files = list()
    config = Config_reader(args.config)
    code = parser_files.file_extension_analyze(args.files, correct_files, config.files)
    if code == Parse_errors.NO_EXTENSION_FILES:
        print(code.value)
        return
    linter = Linter(config, correct_files)


if __name__ == "__main__":
    main()
