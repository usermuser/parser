import argparse

URL = 'https://habr.com/ru/'
TIME_LIMIT = 30  # seconds 10 mins = 600, 2 mins = 120


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store', dest='domain')
    parser.add_argument('-t', action='store', dest='time_limit')
    args = parser.parse_args()
    time_limit = args.time_limit if args.time_limit else TIME_LIMIT
    domain = args.domain if args.domain else URL
    return {'time_limit': float(time_limit), 'domain': str(domain)}


args = {**parse_command_line()}
