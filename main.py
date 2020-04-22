'''Examples:

     python main.py --data-file-path test_data/shows.json --filter-dict '{"name": "Archer"}'
     python main.py --data-file-path test_data/episodes.json --filter-dict '{"season": 5, "number": 3}'
     python main.py --data-file-path test_data/shows.json --filter-dict '{"status": "Ended", "schedule": {"days": ["Saturday"]}}'

     python main.py --endpoint shows --filter-dict '{"name": "Archer"}'
     python main.py --endpoint shows/315/episodes --filter-dict '{"season": 5, "number": 3}'
     python main.py --endpoint shows --filter-dict '{"status": "Ended", "schedule": {"days": ["Saturday"]}}'
'''

import argparse
import json

from tvmaze import TVmaze


def main() -> None:
    # Parse CLI arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', required=False, type=str, help='TVmaze API endpoint (e.g. `shows`)')
    parser.add_argument('--data-file-path', required=False, type=str, help='Use the specified data file instead of downloading it')
    parser.add_argument('--filter-dict', required=True, type=json.loads, help='Filter criteria (e.g. `{"name":"Archer"}`)')
    args = parser.parse_args()

    if (args.endpoint is not None) + (args.data_file_path is not None) != 1:
        raise ValueError('You must specify either `--endpoint` or `--data-file-path` argument, but not both.')

    # Get and filter the results.
    results = TVmaze.get_results(args.endpoint, data_file_path=args.data_file_path)
    filtered_results = results.get_filtered_results(args.filter_dict)

    # Output the filtered results.
    print()
    print(json.dumps(filtered_results, indent=4, sort_keys=True))
    print()


if __name__ == '__main__':
    main()
