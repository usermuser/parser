import argparse

URL = 'https://habr.com/ru/'


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store', dest='domain')
    args = parser.parse_args()
    if args.domain:
        return args.domain
    else:
        return URL
