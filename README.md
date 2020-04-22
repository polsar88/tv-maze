This program can be used to filter shows downloaded from [TV Maze](http://www.tvmaze.com/).

# Prerequisites

This code was tested with Python 3.7.4 on Windows 10 Pro and Python 3.6.9 on Ubuntu 18.04.4 LTS.

First you need to install and/or update dependencies by running this command:
```
pip install -U -r requirements.txt
```

*Note*: On some systems you may need to substitute `pip3` and `python3` for `pip` and `python`, respectively.

# Main Program

To run the main application you need to specify either `--endpoint` argument or `--data-file-path` argument (but not both). Here are a few examples of using `--endpoint`:
```
python main.py --endpoint shows --filter-dict '{"name": "Archer"}'
python main.py --endpoint shows/315/episodes --filter-dict '{"season": 5, "number": 3}'
python main.py --endpoint shows --filter-dict '{"status": "Ended", "schedule": {"days": ["Saturday"]}}'
```

And here are a few example of using `--data-file-path`:
```
python main.py --data-file-path test_data/shows.json --filter-dict '{"name": "Archer"}'
python main.py --data-file-path test_data/episodes.json --filter-dict '{"season": 5, "number": 3}'
python main.py --data-file-path test_data/shows.json --filter-dict '{"status": "Ended", "schedule": {"days": ["Saturday"]}}'
```

*Warning:* Specifying the `shows` endpoint will fetch nearly 200 pages from `http://api.tvmaze.com`, each of which has around 250 shows. This may take a while to run.

# Tests

You can run all tests with the following command:
```
python -m unittest discover .
```

Alternatively, you can run each test case seprately like so:
```
python test_results_episodes.py
python test_results_shows.py
python test_tvmaze.py
```

If you want to see code coverage run the following:
```
coverage run -m unittest discover .
coverage report
```

To generate nice HTML coverage report run
```
coverage html
```
and then open `htmlcov/index.html` in a web browser.

*Note*: If you get `coverage: command not found` error in Ubuntu try to look for it in `/usr/local/bin` or `~/.local/bin` directory. :man_shrugging:
