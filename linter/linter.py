from config_reader.config_reader import Config_reader


class Linter:
    def __init__(self, config: Config_reader, correct_files: list[str]):
        self.config = config
        self.checking_files = correct_files
        self.include_string = None

    def linting(self):
        for file in self.checking_files:
            self.lint_file(file)

    def lint_file(self, curr_file):
        with open(curr_file, "r") as checking_file:
            self.include_string = True
            check_string = checking_file.read()
        for i in range(len(check_string) - 1):
            self.check_double_space()

    def check_double_space(self, first, second):
        if first == " " and second == " ":
            pass

    def call_warning(self, index):
        pass
