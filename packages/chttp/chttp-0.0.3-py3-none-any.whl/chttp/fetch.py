import concurrent.futures
from collections.abc import Iterable
from dataclasses import dataclass

import requests

# https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor


@dataclass
class Fetcher:
    urls: list[str]  # List of urls to be downloaded
    max_workers: int | None = None

    def get_all(self) -> Iterable[requests.Response]:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
        ) as executor:
            results = executor.map(self.fetch_url, self.urls)
            # Start the load operations and mark each future with its URL
            for result in results:
                yield result

    def fetch_url(self, url: str) -> requests.Response:
        return requests.get(url)
