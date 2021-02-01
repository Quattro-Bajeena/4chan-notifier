import requests
import json
import logging
import datetime
import time
import os
from pathlib import Path

from setup import domain, data_path, date_format
from parse_board_data import parse_data_from_filepath

logging.basicConfig(filename=Path(__file__).parent / 'get_board_info.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

if not data_path.is_dir():
    os.mkdir(data_path)

    message = f"data folder not found, created {data_path}"
    logging.info(message)
    print(message)


# returns true if the most recent file is older than the threshold
def check_last_download_time(threshold: datetime.timedelta) -> bool:
    dates = []

    now = datetime.datetime.now()
    for file_path in data_path.glob('*json'):
        _, _, date = parse_data_from_filepath(file_path)


        dates.append(date)
    dates.sort(reverse=True)

    if len(dates) != 0:
        newest_date = dates[0]
        return (now - newest_date) > threshold
    else:
        return True


def download_board_data(boards, endpoints):
    now = datetime.datetime.now().strftime(date_format)
    for board in boards:
        for endpoint_name, endpoint_url in endpoints.items():
            request = f"{domain}/{board}/{endpoint_url}"
            resp = requests.get(request)

            if resp.status_code == 200:
                path = data_path / f"{board}-{endpoint_name} {now}.json"
                with open(path, 'w') as file:
                    json.dump(resp.json(), file, indent=4)

            time.sleep(2)

    logging.info("DONE")


def download_threads_time_check(boards, endpoints, threshold: datetime.timedelta):
    if check_last_download_time(threshold):
        download_board_data(boards, endpoints)
        message = "downloaded the file"
    else:
        message = f"didn't download, files less old than {threshold}"
    logging.info(message)
    print(message)
