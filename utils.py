import argparse

URL = 'https://habr.com/ru/'
TIME_LIMIT = 20  # in seconds,  10mins = 600, 2mins = 120


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store', dest='domain')
    parser.add_argument('-t', action='store', dest='time_limit')
    _args = parser.parse_args()
    time_limit = _args.time_limit if _args.time_limit else TIME_LIMIT
    domain = _args.domain if _args.domain else URL
    return {'time_limit': float(time_limit), 'domain': str(domain)}


args = {**parse_command_line()}
