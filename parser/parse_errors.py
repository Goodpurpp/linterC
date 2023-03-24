from enum import Enum


class Parse_errors(Enum):
    OK = 0
    NO_FILES = "No files"
    NO_EXTENSION_FILES = "No correct files(*.c / *.h)"
    NO_CONFIG = "No config"
