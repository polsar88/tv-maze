import unittest

from test_results import ResultsTest


class ResultsShowsTest(ResultsTest):

    KEYS_TO_CHECK = frozenset({
        'id',
        'name',
        'schedule',
        'status',
    })

    @classmethod
    def setUpClass(cls):
        cls.loadResults('shows')

    def setUp(self):
        self.maxDiff = None

    def test_filter_shows_by_name(self):
        results = self.results.get_filtered_results({'name': 'Archer'})
        self.assertEqual(
            [{
                'id': 315,
                'name': 'Archer',
                'schedule': {'days': ['Wednesday'], 'time': '22:00'},
                'status': 'Running',
            }],
            self._filter_keys(results, self.KEYS_TO_CHECK),
        )

    def test_filter_shows_by_status_and_schedule(self):
        results = self.results.get_filtered_results({
            'status': 'Ended',
            'schedule': {'days': ['Saturday']},
        })
        self.assertEqual(4359, len(results))
        self.assertEqual([
            {'id': 37, 'name': 'Intruders', 'schedule': {'days': ['Saturday'], 'time': '22:00'}, 'status': 'Ended'},
            {'id': 61, 'name': 'Orphan Black', 'schedule': {'days': ['Saturday'], 'time': '22:00'}, 'status': 'Ended'},
            {'id': 74, 'name': 'Hell on Wheels', 'schedule': {'days': ['Saturday'], 'time': '21:00'}, 'status': 'Ended'},
        ], self._filter_keys(results[:3], self.KEYS_TO_CHECK))

    def test_filter_shows_by_schedule_multiple_days(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        results = self.results.get_filtered_results({'schedule': {'days': days}})
        self.assertEqual(3593, len(results))
        self.assertEqual([
            {'id': 250, 'name': 'Kirby Buckets', 'status': 'Ended', 'schedule': {'days': days, 'time': '07:00'}},
            {'id': 265, 'name': 'The Late Show with David Letterman', 'status': 'Ended', 'schedule': {'days': days, 'time': '23:35'}},
            {'id': 290, 'name': 'Adventure Time', 'status': 'Ended', 'schedule': {'days': days, 'time': '19:45'}},
        ], self._filter_keys(results[:3], self.KEYS_TO_CHECK))

    def test_filter_shows_by_schedule_multiple_days_subset(self):
        days = ['Tuesday', 'Thursday']
        results = self.results.get_filtered_results({'schedule': {'days': days}})
        self.assertEqual(4924, len(results))
        self.assertEqual([
            {'id': 243, 'name': 'Conan', 'schedule': {'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'time': '23:00'}, 'status': 'Running'},
            {'id': 247, 'name': 'The Colbert Report', 'schedule': {'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'time': '23:30'}, 'status': 'Ended'},
            {'id': 249, 'name': 'The Daily Show with Jon Stewart', 'schedule': {'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'time': '23:00'}, 'status': 'Ended'},
        ], self._filter_keys(results[:3], self.KEYS_TO_CHECK))

    def test_filter_shows_by_genre_country_day(self):
        results = self.results.get_filtered_results({
            'genres': 'Thriller',
            'network': {'country': {'name': 'France'}},
            'schedule': {'days': 'Saturday'},
        })
        self.assertEqual([{
            'id': 44372,
            'schedule': {'days': ['Saturday'], 'time': ''},
            'status': 'Ended',
            'genres': ['Fantasy', 'Romance', 'Thriller'],
            'name': 'Belph\u00e9gor ou le Fant\u00f4me du Louvre',
        }], self._filter_keys(results, self.KEYS_TO_CHECK | {'genres'}))

    def test_filter_by_multiple_genres(self):
        results = self.results.get_filtered_results({'genres': ['Science-Fiction', 'Drama']})
        self.assertEqual([
            {'name': 'Under the Dome', 'status': 'Ended', 'id': 1, 'schedule': {'days': ['Thursday'], 'time': '22:00'}, 'genres': ['Drama', 'Science-Fiction', 'Thriller']},
            {'name': 'Arrow', 'status': 'Ended', 'id': 4, 'schedule': {'days': ['Tuesday'], 'time': '21:00'}, 'genres': ['Drama', 'Action', 'Science-Fiction']},
            {'name': 'The Flash', 'status': 'Running', 'id': 13, 'schedule': {'days': ['Tuesday'], 'time': '20:00'}, 'genres': ['Drama', 'Action', 'Science-Fiction']},
        ], self._filter_keys(results[:3], self.KEYS_TO_CHECK | {'genres'}))


if __name__ == '__main__':
    unittest.main()
