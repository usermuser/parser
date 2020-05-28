import os

DEPTH = 2
DELAY = 1.0
PAGES_TO_PARSE = 5
URL = 'https://habr.com/ru/'
BASE_DIR = os.getcwd()
PAGES_FOLDER = os.path.join(BASE_DIR, 'saved_pages')
print(f'pages folder: {PAGES_FOLDER}')

# RETRY STRATEGY
RETRY_COUNT = 4
RETRY_TIMEOUT = 2
RETRY = True
REPEAT_TIMEOUT = 2
RETRY_CODES = [413, 429, 500, 502, 503, 504]
