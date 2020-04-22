import json
import logging
import requests
import sys

from typing import (
    List,
    NamedTuple,
    Union,
)

from results import Results


# Initialize logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ResultsPage(NamedTuple):
    is_found: bool
    results: List[dict]


class TVmaze:
    '''This class contains methods to fetch TVmaze results from an API endpoint or file.'''

    API_BASE_URL = 'http://api.tvmaze.com'

    @classmethod
    def get_results(cls, endpoint: Union[None, str], data_file_path: Union[None, str]=None) -> Results:
        '''Returns an instance of Results fetched from either the specified endpoint or file.
        Note that exactly one of (`endpoint`, `data_file_path`) must be a string and the other must be None.'''
        # Do we want to load the data from a file instead of downloading it?
        if data_file_path is not None:
            assert endpoint is None
            return cls.get_results_from_file(data_file_path)

        assert endpoint is not None
        sanitized_endpoint = cls._sanitize_endpoint(endpoint)
        uri = f'{cls.API_BASE_URL}/{sanitized_endpoint}'

        # This is the only paginated API endpoint.
        if endpoint == 'shows':
            return Results(cls._get_paginated_results(uri))

        # Endpoint is not paginated.
        results_page = cls._get_results_page(uri)
        if not results_page.is_found:
            # TODO: Use a more appropriate exception name or define a custom one.
            raise ValueError(f'Resource "{uri}" not found')
        return Results(results_page.results)

    @classmethod
    def get_results_from_file(cls, file_path: str) -> Results:
        '''Reads results from the specified file.'''
        with open(file_path) as fp:
            return Results(json.loads(fp.read()))

    @classmethod
    def _get_paginated_results(cls, uri: str) -> List[dict]:
        '''Returns combined results from all pages.'''
        page = 0
        results = []

        # Keep fetching pages until a page is not found.
        #   http://www.tvmaze.com/api#show-search
        while True:
            results_page = cls._get_results_page(f'{uri}?page={page}')
            if not results_page.is_found:
                break
            results.extend(results_page.results)
            page += 1

        return results

    @classmethod
    def _get_results_page(cls, uri: str) -> ResultsPage:
        # TODO: Implement retry loop in case of network failure.
        logger.info(f'Fetching results from "{uri}"')
        response = requests.get(uri)
        status_code = response.status_code

        # Resource is not found on the server.
        if status_code == requests.status_codes.codes.NOT_FOUND:
            return ResultsPage(
                is_found=False,
                results=[],
            )

        # Some other HTTP "error" occurred.
        # TODO: Implement intelligent handling of common HTTP codes such as redirects.
        if status_code != requests.status_codes.codes.OK:
            # TODO: Use a more appropriate exception name or define a custom one.
            raise ValueError(f'{status_code} returned by querying "{uri}"')

        return ResultsPage(
            is_found=True,
            results=response.json(),
        )

    @classmethod
    def _sanitize_endpoint(cls, endpoint: str) -> str:
        # TODO: Add additional transformations here to make sure the final sanitized endpoint is well-formed.
        return endpoint.strip('/')
