import requests
import json
import logging
import datetime
import time
import os
from pathlib import Path

from boards_info import boards, endpoints, domain, data_folder, date_format
from parse_board_data import parse_data_from_filepath

logging.basicConfig(filename='get_board_info.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

if not Path(data_folder).is_dir():
    os.mkdir(data_folder)

# returns true if the most recent file is older than the threshold
def check_last_download_time(threshold: datetime.timedelta) -> bool:
    data_path = Path(data_folder)
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


def download_board_data():
    now = datetime.datetime.now().strftime(date_format)
    for board in boards:
        for endpoint_name, endpoint_url in endpoints.items():
            request = f"{domain}/{board}/{endpoint_url}"
            resp = requests.get(request)

            if resp.status_code == 200:
                with open(f"{data_folder}\{board}-{endpoint_name} {now}.json", 'w') as file:
                    json.dump(resp.json(), file, indent=4)

            time.sleep(2)

    logging.info("DONE")


def download_threads_time_check(threshold: datetime.timedelta):
    if check_last_download_time(threshold):
        download_board_data()
    else:
        print("files too new")
