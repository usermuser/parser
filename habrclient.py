import json
import logging
import re
import time
from urllib.parse import urlparse
from typing import List

from bs4 import BeautifulSoup
import requests
from settings import (
    DEPTH,
    URL,
    DELAY,
    PAGES_TO_VISIT,
    RETRY_COUNT,
    RETRY_TIMEOUT,
    RETRY,
    REPEAT_TIMEOUT,
    RETRY_CODES,
    PAGES_FOLDER,
    BASE_DIR,
    WORDS_FILE,
    DELAY_BETWEEN_REQUEST,
    POPULAR_WORDS_LIMIT,
    PREPOSITIONS,

)


class BaseParser:
    """Base Parser"""
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    REQUESTS_EXCEPTIONS = (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout,
                           requests.exceptions.ConnectionError, requests.exceptions.HTTPError,
                           requests.exceptions.RequestException)

    def __init__(
            self,
            url=URL,
            retry_count=RETRY_COUNT,
            retry_timeout=RETRY_TIMEOUT,
            retry=RETRY,
            repeat_timeout=REPEAT_TIMEOUT,
            retry_codes=RETRY_CODES,

    ):
        self.url = url
        self.retry_count = retry_count
        self.retry_timeout = retry_timeout
        self.retry = retry
        self.repeat_timeout = repeat_timeout
        self.retry_codes = retry_codes

    @property
    def _set_retries(self) -> int:
        """Check settings for retry strategy"""

        if self.retry:
            return 3 if self.retry_count <= 0 else self.retry_count

        if not self.retry <= 0:
            return 1

    def get(self, url, headers=None, payload=None):
        """GET request with retries"""
        tries = self._set_retries

        while tries > 0:
            try:
                self.logger.info('Делаем запрос по адресу %s.' % url)
                response = requests.get(url)
                if response.status_code == 200:
                    return response
                elif response.status_code in self.retry_codes:
                    self.logger.info('Будем делать повторный запрос так как получили %d.' % response.status_code, url)
                    time.sleep(self.repeat_timeout)
                else:
                    return

            except self.REQUESTS_EXCEPTIONS:
                self.logger.exception('Запрос по адресу %s не удался.' % url)

            except json.decoder.JSONDecodeError:
                self.logger.exception('Запросе по адресу %s не удался: в ответe не JSON: %s' % url, response)

            except Exception:
                self.logger.exception('Внутренняя ошибка!')

            time.sleep(self.retry_timeout)
            self.logger.info('Будем делать повторный запрос так как получили %d.' % response.status_code, url)
            tries -= 1
        self.logger.error('Запрос по адресу %s не удался' % url)
        return


class HabrClient(BaseParser):

    def __init__(self, depth=DEPTH, pages_to_visit=PAGES_TO_VISIT):
        super().__init__()
        self.depth = depth
        self.delay = DELAY
        self.pages_to_visit = pages_to_visit
        self.urls = [[self.url]]
        self.files_to_read = []
        self.prepositions = PREPOSITIONS
        self.frequency = {}
        self.words = WORDS_FILE
        self.visited_urls = []
        self.suffix_number = 0
        self.result_words = []
        self.pupular_words_limit = POPULAR_WORDS_LIMIT

    def save_page(self, _url, _page_content):
        """Save url as html page"""
        _filename = urlparse(_url).netloc
        self.write_to_file(_filename, _page_content, self.suffix_number)
        self.suffix_number += 1
        return

    def get_urls(self):
        """Retrieve urls from self.urls

        we store all urls to work on in self.url
        """
        try:
            _urls_to_save = self.urls.pop()  # [ [url1, url2], [url2.1, url2.2] ... ]
            return _urls_to_save
        except IndexError:  # since we using list of lists in self.urls IndexError means 'we done'
            self.logger.info(f'[INFO] All pages saved')
            return

    def run(self):
        self.clean_words_file()
        while self.depth > 0 and self.pages_to_visit > 0:
            urls = self.get_urls()
            if urls:
                _result = []
                _result_words = []
                for url in urls:
                    time.sleep(DELAY_BETWEEN_REQUEST)
                    page_content = self.get(url)
                    _result.extend(self.extract_links_from_page(page_content))
                    self.save_page(url, page_content)
                    self.visited_urls.append(url)
                    words_as_list = self.filter_words(page_content)
                    self.result_words.extend(words_as_list)
                    self.add_to_words_results_file(words_as_list)
                    self.pages_to_visit -= 1

                    if (self.pages_to_visit <= 0):
                        self.depth = 0
                        self.logger.info(f'Pages counter exhausted, visited {self.visited_urls} urls')
                        self.frequency = self.count_words(self.result_words)  # count words in self.result_words
                        return

                self.depth -= 1
                self.urls.append(_result)
        return

    def extract_links_from_page(self, response):
        result = []
        soup = BeautifulSoup(response.text, 'lxml')
        for raw_link in soup.find_all('a'):
            link = raw_link.get('href')
            # print(f'-------------  link: {link}, \n raw_link: {raw_link}')
            if not link:
                continue
            if link.startswith(self.url) and link not in self.visited_urls:
                result.append(link)
        result = set(result)
        return list(result)

    def filter_words(self, _page_content):
        """Remove prepositions from page content"""
        _soup = BeautifulSoup(_page_content.text, 'lxml')
        _text = _soup.text.lower()
        _words_list = re.findall(r'\w+', _text)
        result = [word for word in _words_list if word not in self.prepositions and not word.isdigit()]
        return result

    def add_to_words_results_file(self, _words_as_list: List) -> None:
        self.logger.info(f'[INFO] Going to write words to file {self.words}')
        with open(self.words, 'a+') as file:
            for word in _words_as_list:
                if word not in self.visited_urls:
                    file.write(f'{word}\n')
        return

    @staticmethod
    def write_to_file(_filename, _page_content, _number):
        _file_path = f'{PAGES_FOLDER}/{_filename}_{_number}.html'
        with open(_file_path, mode='w+') as file:
            try:
                file.write(_page_content.text)
                logging.info(f'Page content succesfully written to {file}')
            except Exception:
                logging.exception(f'[ERROR] Couldn\'t write to file {file}')
        return

    def count_words(self, words_list):
        _frequency = {}
        for word in words_list:
            count = _frequency.get(word, 0)
            _frequency[word] = count + 1
        _frequency = self.sort_words(_frequency)
        return _frequency

    @staticmethod
    def sort_words(_dict):
        return {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1], reverse=True)}

    def clean_words_file(self):
        with open(self.words, 'w') as file:
            file.truncate(0)
        return

    @property
    def popular_words(self):
        if len(self.frequency) == 0:
            self.logger.error('Frequency dictionary is empty')
            return
        result = []
        for word in self.frequency.items():
            result.append(word)
            if len(result) == self.pupular_words_limit:
                return result
        self.logger.error('\nError occured in popular_words_method')
        return

    def show_words(self):
        for word in self.popular_words:
            print(word)

    def __repr__(self):
        return f'Client for {self.url}'


if __name__ == '__main__':
    client = HabrClient()
    client.run()
    client.show_words()