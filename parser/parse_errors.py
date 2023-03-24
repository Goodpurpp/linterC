from enum import Enum


class Parse_errors(Enum):
    OK = 0
    NO_FILES = "No files"
    NO_EXTENSION_FILES = "No extension files"
    NO_CONFIG = "No config"
