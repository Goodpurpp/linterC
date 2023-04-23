import re
from pprint import pprint
from linter.checkers import ops_before_space, double_space
from config_reader.config_reader import ConfigReader
from language.clang_tokens import ClangTokens
from language.clang import Clang
from linter.checkers import is_empty_line


def _count_args(arg, tokens):
    count = 0
    for token in tokens:
        if (arg[2] == token[2] or arg[2] == token[2][0:-2] or
                arg[2][0:-2] == token[2]):
            count += 1
    return count


class Linter:
    def __init__(self, config: ConfigReader, correct_files: list[str]):
        self.config = config
        self.checking_files = correct_files
        self.include_string = None
        self.token_rex = r"(\W+)"
        self.clang_vars = Clang()
        self.curr_file = ""
        self.code = ""

    def linting(self):
        for file in self.checking_files:
            self._lint_file(file)

    def _lint_file(self, curr_file) -> None:
        tokens = []
        self.curr_file = curr_file

        with open(curr_file, "r") as checking_file:
            self.include_string = True
            self.code = checking_file.read().split("\n")
        num = 1
        for cur_str in self.code:
            self.__tokenize_str(cur_str, tokens, num)
            num += 1
        # pprint(t for t in tokens if t[1] == ClangTokens.ARGS)
        self._check(tokens)
        self._not_used_vars(tokens)

    def __tokenize_str(self, curr_str, tokens, num_str) -> None:
        curr_str = curr_str.replace(" ", "- -")
        curr_str = curr_str.replace("(", "-(-")
        curr_str = curr_str.replace(")", "-)-")
        curr_str = curr_str.replace(";", "-;-")
        curr_str = curr_str.replace(",", "-,-")
        str_rex = list(filter(lambda x: x != "", curr_str.split("-")))
        summed_ind = 0
        # print(str_rex)
        if len(str_rex) < 1:
            tokens.append([(num_str, 0), ClangTokens.EMPTY_LINE, "\\n"])
            return
        n = 1
        for val in str_rex:
            summed_ind += len(val)
            tokens.append([(num_str, summed_ind - len(val) + 1),
                           self._check_token(val, tokens), val])
            n += 1

    def __call_warning(self, tokenize):
        print(
            f"{self.curr_file}:{tokenize[0][0]}:{tokenize[0][1]} "
            f"warning: code should be clang-formatted "
            f"[-Wclang-format-violations]")
        print(self.code[tokenize[0][0] - 1])
        print(" " * tokenize[0][1] + "^")

    def _check_token(self, val, tokens) -> ClangTokens:
        token = ClangTokens.VAR
        if val in self.clang_vars.include:
            token = ClangTokens.INCLUDE
        elif val in self.clang_vars.calls:
            token = ClangTokens.CALL
        elif any(val in operators for operators in self.clang_vars.operators):
            token = ClangTokens.OP
        elif val in self.clang_vars.conditional_states:
            token = ClangTokens.STATE
        elif val in self.clang_vars.types:
            token = ClangTokens.TYPE
        elif self.clang_vars.comments[0] in val:
            token = ClangTokens.COMMENT
        elif val in self.clang_vars.pointers_refs:
            token = ClangTokens.PTR
        elif self.clang_vars.comma[0] in val:
            token = ClangTokens.COMMA
        elif any(lib in val for lib in self.clang_vars.libs):
            token = ClangTokens.LIB
        elif val == " ":
            token = ClangTokens.SPACE
        try:
            if (tokens[len(tokens) - 2][1] == ClangTokens.TYPE
                    and len(val) > 2):
                token = ClangTokens.ARGS
            if (tokens[len(tokens) - 2] == ClangTokens.VAR and
                    token == ClangTokens.OP):
                token = ClangTokens.ARGS
        except IndexError:
            pass
        return token

    def _check(self, tokens) -> None:
        count_empty_line = 0
        curr_n_spaces = 0
        summary_len_str = [0, 0]
        for i in range(len(tokens) - 1):
            if tokens[i][0][0] == summary_len_str[0]:
                summary_len_str[1] = tokens[i][0][1] + len(tokens[i][2])
            else:
                summary_len_str = [tokens[i][0][0], tokens[i][0][1]]
            if is_empty_line(tokens[i]):
                count_empty_line += 1
            else:
                count_empty_line = 0
            if summary_len_str[1] > self.config.max_line_len:
                self.__call_warning(tokens[i])
            if count_empty_line > self.config.spaces_before_include:
                self.__call_warning(tokens[i])
                count_empty_line = 0
            if tokens[i][2] == "{":
                curr_n_spaces += 2
            if tokens[i][2] == "}":
                curr_n_spaces -= 2
            if tokens[i][0][1] > curr_n_spaces and double_space(tokens[i],
                                                                tokens[i + 1]):
                self.__call_warning(tokens[i])
            if ops_before_space(tokens[i], tokens[i + 1]):
                self.__call_warning(tokens[i])
            if self._check_var_with_op(tokens[i]):
                self.__call_warning(tokens[i])

    def _check_var_with_op(self, token) -> bool:
        if token[1] != ClangTokens.VAR or token[2][-3:] != "++":
            return False
        print(token)
        return any(op in token[2] for op in self.clang_vars.operators if
                   op != "." and op != "*" and op != "&")

    def _not_used_vars(self, tokens) -> None:
        args = [t for t in tokens if t[1] == ClangTokens.ARGS and
                len([arg for arg in ("argc", "**argv", "main")
                     if arg != t[2]]) == 3]
        # pprint(args)
        for arg in args:
            if _count_args(arg, tokens) < 2:
                self._call_not_use_args(arg)

    def _call_not_use_args(self, tokenize) -> None:
        print(
            f"{self.curr_file}:{tokenize[0][0]}:{tokenize[0][1]} "
            f"warning:this arg or func not used")
        print(self.code[tokenize[0][0] - 1])
        print(" " * tokenize[0][1] + "^")
