import re
from pprint import pprint
from linter.checkers import *
from config_reader.config_reader import Config_reader
from language.clang_tokens import Clang_tokens
from language.clang import Clang
from linter.checkers import is_empty_line


class Linter:
    def __init__(self, config: Config_reader, correct_files: list[str]):
        self.config = config
        self.checking_files = correct_files
        self.include_string = None
        self.token_rex = r"(\W+)"
        self.clang_vars = Clang()
        self.curr_file = ""
        self.code = ""

    def linting(self):
        for file in self.checking_files:
            self.__lint_file(file)

    def __lint_file(self, curr_file) -> None:
        tokens = []
        self.curr_file = curr_file
        with open(curr_file, "r") as checking_file:
            self.include_string = True
            self.code = checking_file.read().split("\n")
        num = 1
        for cur_str in self.code:
            self.__tokenize_str(cur_str, tokens, num)
            num += 1
        self.__check(tokens)
        # pprint(tokens)

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
            tokens.append([(num_str, 0), Clang_tokens.EMPTY_LINE, "\\n"])
            return
        n = 1
        for val in str_rex:
            summed_ind += len(val)
            tokens.append(
                [(num_str, summed_ind - len(val) + 1), self.__check_token(val),
                 val])
            n += 1

    def __call_warning(self, tokenize):
        print(
            f"{self.curr_file}:{tokenize[0][0]}:{tokenize[0][1]} "
            f"warning: code should be clang-formatted "
            f"[-Wclang-format-violations]")
        print(self.code[tokenize[0][0] - 1])
        print(" " * tokenize[0][1] + "^")

    def __check_token(self, val) -> Clang_tokens:
        token = Clang_tokens.VAR
        if val in self.clang_vars.include:
            token = Clang_tokens.INCLUDE
        elif val in self.clang_vars.calls:
            token = Clang_tokens.CALL
        elif any(val in operators for operators in self.clang_vars.operators):
            token = Clang_tokens.OP
        elif val in self.clang_vars.conditional_states:
            token = Clang_tokens.STATE
        elif val in self.clang_vars.types:
            token = Clang_tokens.TYPE
        elif self.clang_vars.comments[0] in val:
            token = Clang_tokens.COMMENT
        elif val in self.clang_vars.pointers_refs:
            token = Clang_tokens.PTR
        elif self.clang_vars.comma[0] in val:
            token = Clang_tokens.COMMA
        elif any(lib in val for lib in self.clang_vars.libs):
            token = Clang_tokens.LIB
        elif val == " ":
            token = Clang_tokens.SPACE
        return token

    def __check(self, tokens) -> None:
        count_empty_line = 0
        curr_n_spaces = 0
        summary_len_str = [0, 0]
        for i in range(len(tokens) - 1):
            if tokens[i][0][0] == summary_len_str[0]:
                summary_len_str[1] = tokens[i][0][1] + len(tokens[i][2])
            else:
                summary_len_str = [tokens[i][0][0], tokens[i][0][1]]
            if summary_len_str[1] > self.config.max_line_len:
                self.__call_warning(tokens[i])
            if is_empty_line(tokens[i]):
                count_empty_line += 1
            else:
                count_empty_line = 0
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
            if self.__check_var_with_op(tokens[i]):
                self.__call_warning(tokens[i])

    def __check_var_with_op(self, token) -> bool:
        if token[1] != Clang_tokens.VAR or token[2][-3:] != "++":
            return False
        return any(op in token[2] for op in self.clang_vars.operators if
                   op != "." and op != '*' and op != "&")
