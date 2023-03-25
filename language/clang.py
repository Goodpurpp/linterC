class Clang:
    calls = ["return"]
    operators = ["+-*:;/%=!&|?()[]{}"]
    types = ["int", "short", "long", "char", "float", "double", "struct", "void"]
    conditional_states = ["if", "else", "while", "for", "do", "case", "continue", "break"]
    comments = ["//"]
    points = ["&", "*"]
    pointers_refs = [point + typeof for point in points for typeof in types]
