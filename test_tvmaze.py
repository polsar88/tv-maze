import builtins
import requests
import unittest
from unittest.mock import (
    call,
    patch,
)

from results import Results
from tvmaze import TVmaze


class MockResponse:

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TvMazeTest(unittest.TestCase):

    TEST_FILE_FILE = 'test_data/episodes.json'

    def test_get_results_from_file(self):
        results = TVmaze.get_results_from_file(self.TEST_FILE_FILE)
        self.assertEqual(110, results.get_num_results())

    @patch.object(requests, 'get')
    @patch.object(builtins, 'open')
    def test_get_results_both_endpoint_and_file_path_are_none(self, open_mock, get_mock):
        self.assertRaises(AssertionError, TVmaze.get_results, None, None)
        self.assertFalse(open_mock.called)
        self.assertFalse(get_mock.called)

    @patch.object(requests, 'get')
    @patch.object(builtins, 'open')
    def test_get_results_neither_endpoint_nor_file_path_is_none(self, open_mock, get_mock):
        self.assertRaises(AssertionError, TVmaze.get_results, 'shows', 'path/to/file')
        self.assertFalse(open_mock.called)
        self.assertFalse(get_mock.called)

    @patch.object(requests, 'get')
    def test_get_results_load_from_file(self, get_mock):
        results = TVmaze.get_results(None, self.TEST_FILE_FILE)
        self.assertEqual(110, results.get_num_results())
        self.assertFalse(get_mock.called)

    @patch.object(requests, 'get', return_value=MockResponse(None, 404))
    def test_get_results_non_paginated_endpoint_not_found(self, get_mock):
        self.assertRaisesRegex(ValueError, 'not found', TVmaze.get_results, 'shows/315/episodes')
        get_mock.assert_called_once_with('http://api.tvmaze.com/shows/315/episodes')

    @patch.object(requests, 'get', return_value=MockResponse(None, 400))
    def test_get_results_non_paginated_endpoint_error(self, get_mock):
        self.assertRaisesRegex(ValueError, '400 returned', TVmaze.get_results, 'shows/315/episodes')
        get_mock.assert_called_once_with('http://api.tvmaze.com/shows/315/episodes')

    @patch.object(requests, 'get', return_value=MockResponse([{'a': 1}, {'b': 2}], 200))
    def test_get_results_non_paginated_endpoint_ok(self, get_mock):
        self.assertEqual(
            Results([{'a': 1}, {'b': 2}]),
            TVmaze.get_results('shows/315/episodes')
        )
        get_mock.assert_called_once_with('http://api.tvmaze.com/shows/315/episodes')

    @patch.object(requests, 'get', return_value=MockResponse(None, 404))
    def test_get_results_paginated_endpoint_no_pages(self, get_mock):
        self.assertEqual(Results([]), TVmaze.get_results('shows'))
        get_mock.assert_called_once_with('http://api.tvmaze.com/shows?page=0')

    @patch.object(requests, 'get', side_effect=[
        MockResponse([{'a': 1}, {'b': 2}], 200),
        MockResponse(None, 404),
    ])
    def test_get_results_paginated_endpoint_one_page(self, get_mock):
        self.assertEqual(
            Results([{'a': 1}, {'b': 2}]),
            TVmaze.get_results('shows')
        )
        self.assertEqual(2, get_mock.call_count)
        get_mock.assert_has_calls([
            call('http://api.tvmaze.com/shows?page=0'),
            call('http://api.tvmaze.com/shows?page=1'),
        ], any_order=False)

    @patch.object(requests, 'get', side_effect=[
        MockResponse([{'a': 1}, {'b': 2}], 200),
        MockResponse(None, 400),
    ])
    def test_get_results_paginated_endpoint_error_after_first_page(self, get_mock):
        self.assertRaisesRegex(ValueError, '400 returned', TVmaze.get_results, 'shows')
        self.assertEqual(2, get_mock.call_count)
        get_mock.assert_has_calls([
            call('http://api.tvmaze.com/shows?page=0'),
            call('http://api.tvmaze.com/shows?page=1'),
        ], any_order=False)

    @patch.object(requests, 'get', side_effect=[
        MockResponse([{'b': 2}], 200),
        MockResponse([{'d': 6}, {'cc': 5, 'E': 11}], 200),
        MockResponse(None, 404),
    ])
    def test_get_results_paginated_endpoint_two_pages(self, get_mock):
        self.assertEqual(
            Results([{'b': 2}, {'d': 6}, {'cc': 5, 'E': 11}]),
            TVmaze.get_results('shows')
        )
        self.assertEqual(3, get_mock.call_count)
        get_mock.assert_has_calls([
            call('http://api.tvmaze.com/shows?page=0'),
            call('http://api.tvmaze.com/shows?page=1'),
            call('http://api.tvmaze.com/shows?page=2'),
        ], any_order=False)


if __name__ == '__main__':
    unittest.main()
