from language.clang_tokens import ClangTokens


def is_empty_line(token):
    return token[1] == ClangTokens.EMPTY_LINE


def ops_before_space(first, second):
    if first[0][0] != second[0][0]:
        return False
    if (first[2] == "(" and (second[1] == ClangTokens.VAR
                             or second[1] == ClangTokens.TYPE)):
        return False
    if ((first[1] == ClangTokens.VAR or first[1] == ClangTokens.TYPE) and
            second[2] == ")"):
        return False
    if first[2] == ")" and second[2] == ";":
        return False
    if first[1] == ClangTokens.VAR and (second[2] == ";" or second[2] == "("):
        return False
    if first[1] == ClangTokens.VAR:
        return (second[1] != ClangTokens.SPACE and
                second[1] != ClangTokens.COMMA and
                second[1] != ClangTokens.EMPTY_LINE)
    if (first[1] == ClangTokens.OP or first[1] == ClangTokens.STATE or
            first[1] == ClangTokens.COMMA):
        return second[1] != ClangTokens.SPACE
    return False


def double_space(first, second):
    return (first[1] == ClangTokens.SPACE and
            second[1] == ClangTokens.SPACE and first[0][0] == second[0][0])
