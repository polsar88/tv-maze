import unittest

from tvmaze import TVmaze


class ResultsTest(unittest.TestCase):

    @classmethod
    def loadResults(cls, base_file_name):
        cls.results = TVmaze.get_results_from_file(f'test_data/{base_file_name}.json')

    @classmethod
    def _filter_keys(cls, list_of_dicts, keys):
        return [{k: dct[k] for k in keys if k in dct} for dct in list_of_dicts]
