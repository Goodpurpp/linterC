from argparse import ArgumentParser


def cli_parse() -> ArgumentParser.parse_args:
    parser_cli = ArgumentParser(description="Simple linter for C language")
    parser_cli.add_argument("-config", help="config for lint", type=str)
    parser_cli.add_argument("-files", help="files", type=str, nargs='*')
    return parser_cli.parse_args()
