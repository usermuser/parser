import json
import logging
import time
from urllib.parse import urlparse
from typing import List

from bs4 import BeautifulSoup
import requests
from settings import (
    DEPTH,
    URL,
    DELAY,
    PAGES_TO_PARSE,
    RETRY_COUNT,
    RETRY_TIMEOUT,
    RETRY,
    REPEAT_TIMEOUT,
    RETRY_CODES,
    PAGES_FOLDER,
    BASE_DIR,

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

    def __init__(self, depth=DEPTH, pages_to_parse=PAGES_TO_PARSE):
        super().__init__()
        self.depth = depth
        self.pages = List
        self.delay = DELAY
        self.pages_to_parse = pages_to_parse
        self.urls = [[self.url]]


    def run(self):
        try:
            urls_to_save = self.urls.pop()
            self.depth -= 1
            self.save_pages(urls_to_save)
        except IndexError:
            print(f'Все страницы сохранены')
            # Open files
            # Count words
        return

    def save_pages(self, _urls):
        for url in _urls:
            page_content = self.get_page_content(url)
            pagename = urlparse(url).netloc
            self.write_to_file(pagename, page_content)
            self.pages_to_parse -= 1
            if self.pages_to_parse <= 0:
                return
        return

    @staticmethod
    def write_to_file(_filename, _page_content):
        __file_path = f'{PAGES_FOLDER}/{_filename}.html'
        with open(__file_path, mode='w+') as file:
            try:
                file.write(_page_content.text)
            except Exception as e:
                print(f'Exception occured: {e}')
        return

    def get_page_content(self, _url):
        return self.get(_url)

    # def extract_urls(self, response):
    #     result = []
    #
    #     for raw_link in soup.find_all('a'):
    #         link = raw_link.get('href')
    #         if link.startswith(self.url) and link != self.url:
    #             result.append(link)
    #     return result

    def __repr__(self):
        return f'Client for {self.url}'


if __name__ == '__main__':
    client = HabrClient()
    client.run()
