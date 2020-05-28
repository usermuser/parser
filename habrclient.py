import time
from urllib.parse import urlparse
from typing import List

from bs4 import BeautifulSoup
import requests as req
from settings import (
    DEPTH,
    URL,
    DELAY,
    PAGES_TO_PARSE,
)


class HabrClient:
    def __init__(self, url=URL, depth=DEPTH, quantity=PAGES_TO_PARSE):
        self.url = url
        self.depth = depth
        self.pages = List
        self.delay = DELAY
        self.quantity = quantity

    def parse(self):
        while self.depth > 0 or self.quantity > 0:
            time.sleep(self.delay)
            self.pages.append()
            # do some work
            self.quantity -= 1
            self.depth -= 1
        return



    def _remove_slash(self):
        pass

    def from_same_domain(self):
        pass

    def __repr__(self):
        return f'Client for {self.url}'


if __name__ == '__main__':
    client = HabrClient()
    print(client)
