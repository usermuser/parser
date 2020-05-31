import os
from utils import args

URL = args['domain']
TIME_LIMIT = args['time_limit']
BASE_DIR = os.getcwd()
PAGES_FOLDER = os.path.join(BASE_DIR, 'saved_pages')
WORDS_FILE = 'words.txt'
DELAY_BETWEEN_REQUEST = 0.3
POPULAR_WORDS_LIMIT = 10
PREPOSITIONS = ('а-ля', 'без', 'безо', 'близ', 'в', 'вблизи', 'ввиду', 'вглубь', 'взамен',
                'включая', 'вне', 'во', 'вроде', 'для', 'до', 'за', 'из', 'из-за', 'из-под',
                'изо', 'к', 'ко', 'кроме', 'меж', 'между', 'на', 'над', 'ниже', 'о', 'об',
                'обо', 'около', 'от', 'перед', 'по', 'под', 'подо', 'при', 'про', 'ради', 'с', 'сверх')

# RETRY STRATEGY
RETRY_COUNT = 4
RETRY_TIMEOUT = 2
RETRY = True
REPEAT_TIMEOUT = 2
RETRY_CODES = [413, 429, 500, 502, 503, 504]
