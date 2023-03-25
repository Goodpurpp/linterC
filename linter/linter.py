import re
from pprint import pprint

from config_reader.config_reader import Config_reader
from language.clang_tokens import Clang_tokens
from language.clang import Clang


class Linter:
    def __init__(self, config: Config_reader, correct_files: list[str]):
        self.config = config
        self.checking_files = correct_files
        self.include_string = None
        self.token_rex = r"(\W+)"
        self.clang_vars = Clang()

    def linting(self):
        for file in self.checking_files:
            self.lint_file(file)

    def lint_file(self, curr_file) -> None:
        tokens = []
        with open(curr_file, "r") as checking_file:
            self.include_string = True
            check_str = checking_file.read().split("\n")
        num = 1
        for cur_str in check_str:
            self.tokenize_str(cur_str, tokens, num)
            num += 1
        pprint(tokens)

    def tokenize_str(self, curr_str, tokens, num_str) -> None:
        curr_str = curr_str.replace(" ", "- -")
        curr_str = curr_str.replace("(", "-(-")
        curr_str = curr_str.replace(")", "-)-")
        curr_str = curr_str.replace(";", "-;-")
        str_rex = list(filter(lambda x: x != "", curr_str.split("-")))
        summed_ind = 0
        if len(str_rex) == 1:
            tokens.append([(num_str, 0), Clang_tokens.EMPTY_LINE.value, "\\n"])
            return
        n = 1
        for val in str_rex:
            summed_ind += len(val)
            tokens.append([(num_str, summed_ind), self.check_token(val), val])
            n += 1

    def call_warning(self, index):
        pass

    def check_token(self, val) -> Clang_tokens:
        token = Clang_tokens.VAR
        if val in self.clang_vars.include:
            token = Clang_tokens.INCLUDE
        elif val in self.clang_vars.calls:
            token = Clang_tokens.CALL
        elif any(val in operators for operators in self.clang_vars.operators):
            token = Clang_tokens.OP
        elif val in self.clang_vars.types:
            token = Clang_tokens.TYPE
        elif self.clang_vars.comments[0] in val:
            token = Clang_tokens.COMMENT
        elif val in self.clang_vars.pointers_refs:
            token = Clang_tokens.PTR
        elif val == " ":
            token = Clang_tokens.SPACE
        return token
