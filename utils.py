import argparse

URL = 'https://habr.com/ru/'


def parse_command_line():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-t', action='store', dest='token')
    parser.add_argument('-d', action='store', dest='domain')
    args = parser.parse_args()
    # token = args.token if args.token else DEFAULT_TOKEN
    # excel_folder = check_path(args, excel_folder)
    if args.domain:
        return args.domain
    else:
        return URL
