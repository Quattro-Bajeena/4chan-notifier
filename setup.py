import yaml
from pathlib import Path

domain = "https://a.4cdn.org"

endpoints = {
    "Catalog": "catalog.json",
    # "Archive": "archive.json",
    # "Threads": "threads.json"
}


root_folder = Path(__file__).parent
data_folder = 'board_data'
data_path = root_folder / data_folder
date_format = '%Y-%m-%d--%H-%M-%S'

# in lowercase

with open(root_folder / 'config.yml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)
    boards = config['boards']
    searched_words = config['searched_words']


