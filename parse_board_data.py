import json
import html
from pathlib import Path
import datetime

from setup import date_format


# catalog - json response from 4chan API, returns a list of threads
def thread_list(catalog):
    parsed = []
    for page in catalog:
        for thread in page['threads']:
            parsed.append(thread)
    return parsed


def parse_data_from_filepath(filepath: Path):
    # board_data/m-Catalog 2021-01-14--15-30.json
    # returns m, Catalog, 2021/01/14 15:30 as datetime.datetime

    name, date = filepath.stem.split()
    board, endpoint_type = name.split('-')
    date = datetime.datetime.strptime(date, date_format)

    return board, endpoint_type, date


# returns tuple of board and list of threads
def get_threads_from_file(filepath: Path) -> (str, list):
    board, endpoint_type, date = parse_data_from_filepath(filepath)
    with open(filepath, 'r') as file:
        data = json.load(file)
        parsed_threads = thread_list(data)
    return board, parsed_threads


# returns a dict that as a keys has names of boards and vaules a list of threads
def get_threads(boards, data_path: Path) -> dict:
    catalog_files = {}

    # getting date and path info of every json file that is in data folder
    for file_path in data_path.glob('*json'):
        board, endpoint_type, date = parse_data_from_filepath(file_path)

        if endpoint_type != 'Catalog' or board not in boards:
            continue

        if board not in catalog_files:
            catalog_files[board] = [(date, file_path)]
        else:
            catalog_files[board].append((date, file_path))

    # catalog_files = {board : [(date, file_path), ...], board: ...}

    # only leaving two most recent files, discarding the date info afterwards
    for board in catalog_files:
        catalog_files[board].sort(key=lambda f: f[0], reverse=True)
        catalog_files[board] = catalog_files[board][:2]
        catalog_files[board] = [file[1] for file in catalog_files[board]]

    threads_summary = {}
    for board, file_paths in catalog_files.items():
        threads_summary[board] = {}

        current_threads = get_threads_from_file(file_paths[0])[1]
        current_ids = [thread['no'] for thread in current_threads]


        if len(file_paths) > 1:
            previous_threads = get_threads_from_file(file_paths[1])[1]
            previous_ids = [thread['no'] for thread in previous_threads]

            new_ids = list(set(current_ids).difference(previous_ids))
            current_ids = list(set(current_ids).difference(new_ids))
            new_threads = [thread for thread in current_threads if thread['no'] in new_ids]
        else:
            new_threads = current_threads
            current_threads = []



        threads_summary[board]['new'] = new_threads
        threads_summary[board]['current'] = current_threads

    # print(len(threads_summary['m']['new']))
    # print(len(threads_summary['m']['current']))

    return threads_summary


def filter_threads(threads, keywords: list, check_comment=True):
    filtered = []
    for thread in threads:
        accept = False

        for keyword in keywords:
            if check_comment:
                if 'sub' in thread and keyword in thread['sub'].lower():
                    accept = True
                if 'com' in thread and keyword in thread['com'].lower():
                    accept = True

            else:
                if 'sub' in thread and keyword in thread['sub'].lower():
                    accept = True

        if accept:
            filtered.append(thread)
    return filtered


def print_threads(threads):
    for thread in threads:
        if 'sub' in thread:
            print(thread['sub'])
        elif 'com' in thread:
            print("NO SUBJECT: " + thread['com'][:40] + (thread['com'][40:] and '..'))
        else:
            print("NO SUBJECT OR COMMENT")


def threads_to_str(threads, punctuator = '') -> str:
    output = ''
    for thread in threads:
        if 'sub' in thread:
            thread['sub'] = html.unescape(thread['sub'])
            output += f"{punctuator} {thread['sub']}\n"
        elif 'com' in thread:
            thread['com'] = html.unescape(thread['com'])
            output += punctuator + ' ' +"NO SUBJECT: " + thread['com'][:40] + (thread['com'][40:] and '..') + '\n'
            output += f"{punctuator} NO SUBJECT: {thread['com'][:40]}{(thread['com'][40:] and '..')}\n"
        else:
            output += f"{punctuator} NO SUBJECT OR COMMENT\n"
    return output
