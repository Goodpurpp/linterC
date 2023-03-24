from config_reader.config_reader import Config_reader
from parser.parse_errors import Parse_errors

MIN_FILES = 1
INDEX_CONFIG_FILE = 2
EXTENSION_CONFIG = ".yaml"


class Parser:
    @staticmethod
    def parsing(arguments: list[str]) -> (int, str):
        if len(arguments) < MIN_FILES:
            return Parse_errors.NO_FILES
        return Parse_errors.OK

    @staticmethod
    def check_config_file(config: str):
        if config is None:
            return Parse_errors.NO_CONFIG
        if EXTENSION_CONFIG in config:
            return Parse_errors.OK

    @staticmethod
    def file_extension_analyze(files: [str], correct_files: [str], config: Config_reader) -> (int, str):
        for file in files:
            if any(extension in file for extension in config.files):
                correct_files.append(file)
        if len(correct_files):
            return Parse_errors.OK
        return Parse_errors.NO_EXTENSION_FILES
