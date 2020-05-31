import json
import logging
import re
import time
from typing import List

from bs4 import BeautifulSoup
import requests
from settings import (
    URL,
    RETRY_COUNT,
    RETRY_TIMEOUT,
    RETRY,
    REPEAT_TIMEOUT,
    RETRY_CODES,
    WORDS_FILE,
    DELAY_BETWEEN_REQUEST,
    POPULAR_WORDS_LIMIT,
    PREPOSITIONS,
    TIME_LIMIT,

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

    def __init__(self):
        super().__init__()
        self.prepositions = PREPOSITIONS
        self.frequency = {}
        self.words = WORDS_FILE
        self.visited_urls = []
        self.result_words = []
        self.popular_words_limit = POPULAR_WORDS_LIMIT
        self.time_limit = TIME_LIMIT
        self.urls_to_visit = []

    def is_valid(self, url) -> List:
        if not url.startswith('http'):
            url = f'https://{url}'
        try:
            response = self.get(url)
            time.sleep(DELAY_BETWEEN_REQUEST)
            return [url]

        except self.REQUESTS_EXCEPTIONS:
            self.logger.error(f'\nProvided domain is not valid, tried with "https:" prefix, no luck')
            return []

    def run(self):
        self.urls_to_visit = self.is_valid(self.url)
        if self.urls_to_visit:
            start = time.time()

            for url in self.urls_to_visit:
                time.sleep(DELAY_BETWEEN_REQUEST)

                page_content = self.get(url)
                _extracted_urls = self.extract_links_from_page(page_content)
                self.urls_to_visit.extend(_extracted_urls)

                self.visited_urls.append(url)
                words_as_list = self.filter_words(page_content)
                self.result_words.extend(words_as_list)
                self.frequency = self.count_words(self.result_words)

                elapsed = time.time() - start
                if elapsed > self.time_limit:
                    self.logger.info(
                        f'[INFO] Time is over. Elapsed time: {elapsed}, time limit: {self.time_limit}')
                    return

                elif len(self.urls_to_visit) == 0:
                    self.logger.info(f'\nNo more urls to visit, visited: \n {self.visited_urls} urls')

                    return
        else:
            self.logger.debug(f'\nNo more urls to visit')
        return

    def extract_links_from_page(self, response):
        result = []
        soup = BeautifulSoup(response.text, 'lxml')

        for raw_link in soup.find_all('a'):
            link = raw_link.get('href')
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

    @property
    def popular_words(self):
        if len(self.frequency) == 0:
            self.logger.error('Frequency dictionary is empty')
            return
        result = []
        for word in self.frequency.items():
            result.append(word)
            if len(result) == self.popular_words_limit:
                return result
        self.logger.error('\nError occured in popular_words_method')
        return

    def show_words(self):
        if self.popular_words:
            for word in self.popular_words:
                print(word)
            return
        else:
            self.logger.error('There is no words to count')
            return

    def __repr__(self):
        return f'Client for {self.url}'


if __name__ == '__main__':
    client = HabrClient()
    client.run()
    client.show_words()
