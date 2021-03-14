from pathlib import Path

domain = "https://a.4cdn.org"
boards = ("m","a")
endpoints = {
    "Catalog": "catalog.json",
    # "Archive": "archive.json",
    # "Threads": "threads.json"
}

data_folder = 'board_data'
data_path = Path(__file__).parent / data_folder
date_format = '%Y-%m-%d--%H-%M-%S'

# in lowercase
searched_words = ['art', 'draw', 'sing']
