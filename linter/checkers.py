from language.clang_tokens import Clang_tokens


def is_empty_line(token) -> bool:
    return token[1] == Clang_tokens.EMPTY_LINE


def ops_before_space(first, second) -> bool:
    if first[0][0] != second[0][0]:
        return False
    if first[2] == "(" and (
            second[1] == Clang_tokens.VAR or second[1] == Clang_tokens.TYPE):
        return False
    if (first[1] == Clang_tokens.VAR or first[1] == Clang_tokens.TYPE) and \
            second[2] == ")":
        return False
    if first[2] == ")" and second[2] == ";":
        return False
    if first[1] == Clang_tokens.VAR and (second[2] == ";" or second[2] == "("):
        return False
    if first[1] == Clang_tokens.VAR:
        return second[1] != Clang_tokens.SPACE and second[
            1] != Clang_tokens.COMMA and second[
            1] != Clang_tokens.EMPTY_LINE
    if first[1] == Clang_tokens.OP or first[1] == Clang_tokens.STATE or \
            first[1] == Clang_tokens.COMMA:
        return second[1] != Clang_tokens.SPACE
    return False


def double_space(first, second) -> bool:
    return first[1] == Clang_tokens.SPACE and second[
        1] == Clang_tokens.SPACE and first[0][0] == second[0][0]
