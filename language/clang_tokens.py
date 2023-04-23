from enum import Enum


class ClangTokens(Enum):
    FUNC = "FUNC"
    OP = "OPERATOR"
    TYPE = "TYPE"
    STATE = "CONDITIONAL STATES"
    COMMENT = "COMMENT"
    PTR = "POINTER OR REF"
    VAR = "VAR"
    SPACE = "SPACE"
    EMPTY_LINE = "EMPTY LINE"
    INCLUDE = "INCLUDE"
    OTHER = "OTHER"
    CALL = "CALL"
    LIB = "LIBRARY"
    COMMA = "COMMA"
    ARGS = "ARGS"
