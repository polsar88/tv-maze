from typing import List


class Results:
    '''This class represents the results of querying an TVmaze API endpoint.'''

    def __init__(self, results: List[dict]) -> None:
        self._results = results

    def __eq__(self, other: 'Results') -> bool:
        return self._results == other._results

    def get_num_results(self) -> int:
        '''Returns the total number of results.'''
        return len(self._results)

    def get_filtered_results(self, filter_dict: dict) -> List[dict]:
        '''Returns a list of results filtered by the specified dict.'''
        return list(filter(
            lambda result_dict: self._is_match(result_dict, filter_dict),
            self._results
        ))

    @classmethod
    def _is_match(cls, result_dict: dict, filter_dict: dict) -> bool:
        '''Returns True if and only if the result dict matches the filter dict.'''
        # We match on every filter key in turn.
        for filter_key, filter_val in filter_dict.items():
            # If the filter key does not occur in the result dict it's not a match.
            if filter_key not in result_dict:
                return False
            result_val = result_dict[filter_key]

            # If both result and filter values are dicts, make a recursive call on them.
            if isinstance(result_val, dict) and isinstance(filter_val, dict):
                if not cls._is_match(result_val, filter_val):
                    return False
                continue

            # If one value is a list, we match if and only if the filter list is a subset of the result list.
            is_result_val_list = isinstance(result_val, list)
            is_filter_val_list = isinstance(filter_val, list)
            if is_result_val_list or is_filter_val_list:
                result_set = set(result_val) if is_result_val_list else {result_val}
                filter_set = set(filter_val) if is_filter_val_list else {filter_val}
                if not (filter_set <= result_set):
                    return False
                continue

            # Finally, we match if and only if the values are equal.
            if filter_val != result_val:
                return False

        return True
