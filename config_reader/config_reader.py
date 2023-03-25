import yaml


class Config_reader:
    def __init__(self, config: str) -> None:
        with open(config, "r") as config_file:
            data = yaml.safe_load(config_file)
        self.files = data['files']
        self.max_line_len = data['max-line-length']
        self.spaces_before_include = data['spaces-before-include']
        self.clang_format = data['format']
