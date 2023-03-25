class Clang:
    def __init__(self):
        self.include = "#include"
        self.calls = ["return"]
        self.operators = ["+", "-", "*", ":", ";", "/", "%", "=", "!", "&", "|", "?", "(", ")", "[", "]", "{", "}", ".",
                          "->", "=="]
        self.comma = [","]
        self.types = ["int", "short", "long", "char", "float", "double",
                      "struct",
                      "void"]
        self.conditional_states = ["if", "else", "while", "for", "do", "case",
                                   "continue", "break", "switch"]
        self.comments = ["//"]
        points = ["&", "*"]
        self.pointers_refs = [point + typeof for point in points for typeof in
                              self.types]
        self.libs = [".c", ".h"]
