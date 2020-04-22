import unittest

from test_results import ResultsTest


class ResultsEpisodesTest(ResultsTest):

    KEYS_TO_CHECK = frozenset({
        'airtime',
        'id',
        'name',
        'number',
        'season',
    })

    @classmethod
    def setUpClass(cls):
        cls.loadResults('episodes')

    def test_filter_episodes_by_non_existent_key(self):
        results = self.results.get_filtered_results({'seasons': 6})
        self.assertEqual([], results)

    def test_filter_episodes_by_season_and_number(self):
        results = self.results.get_filtered_results({'season': 5, 'number': 3})
        self.assertEqual(
            [{
                'airtime': '22:00',
                'id': 31085,
                'name': 'A Debt of Honor',
                'number': 3,
                'season': 5,
            }],
            self._filter_keys(results, self.KEYS_TO_CHECK),
        )

    def test_filter_episodes_by_airtime(self):
        results = self.results.get_filtered_results({'airtime': '22:30'})
        self.assertCountEqual([
            {'airtime': '22:30', 'id': 31034, 'name': 'Mole Hunt', 'number': 1, 'season': 1},
            {'airtime': '22:30', 'id': 31057, 'name': 'Heart of Archness: Part I', 'number': 1, 'season': 3},
            {'airtime': '22:30', 'id': 31058, 'name': 'Heart of Archness: Part II', 'number': 2, 'season': 3},
            {'airtime': '22:30', 'id': 31059, 'name': 'Heart of Archness: Part III', 'number': 3, 'season': 3},
        ], self._filter_keys(results, self.KEYS_TO_CHECK))


if __name__ == '__main__':
    unittest.main()
