from parser.parse_errors import ParseErrors
from parser.parsers_vars import MIN_FILES, INDEX_CONFIG_FILE, EXTENSION_CONFIG


class Parser:
    @staticmethod
    def parsing(arguments: list[str]) -> (int, str):
        if arguments is None:
            return ParseErrors.NO_FILES
        if len(arguments) < MIN_FILES:
            return ParseErrors.NO_FILES
        return ParseErrors.OK

    @staticmethod
    def check_config_file(config: str):
        if config is None:
            return ParseErrors.NO_CONFIG
        if EXTENSION_CONFIG in config:
            return ParseErrors.OK
        return ParseErrors.NO_CONFIG

    @staticmethod
    def file_extension_analyze(files: [str], correct_files: [str],
                               config_files) -> (int, str):
        for file in files:
            if any(extension in file for extension in config_files):
                correct_files.append(file)
        if len(correct_files):
            return ParseErrors.OK
        return ParseErrors.NO_EXTENSION_FILES
