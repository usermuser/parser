import os
from utils import parse_command_line

DEPTH = 29999
AMOUNT_PAGES_TO_VISIT = 59999
URL = parse_command_line()
BASE_DIR = os.getcwd()
PAGES_FOLDER = os.path.join(BASE_DIR, 'saved_pages')
WORDS_FILE = 'words.txt'
DELAY_BETWEEN_REQUEST = 0.3
POPULAR_WORDS_LIMIT = 10
TIME_LIMIT = 30  # seconds 10 mins = 600, 2 mins = 120
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
