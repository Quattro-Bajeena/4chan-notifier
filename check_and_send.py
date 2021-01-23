import datetime

from parse_board_data import get_threads, filter_threads, threads_to_str
from boards_info import data_folder, searched_words
from get_board_data import download_threads_time_check, download_board_data
from pushover import send_notification


def check_boards(send_only_if_new: bool):
    download_threads_time_check(datetime.timedelta(minutes=30))

    threads = get_threads(data_folder)
    title = "Current threads with searched words"
    message = ''

    any_new = False
    for board in threads:
        threads[board]['current'] = filter_threads(threads[board]['current'], searched_words, check_comment=False)
        threads[board]['new'] = filter_threads(threads[board]['new'], searched_words, check_comment=False)

        if len(threads[board]['new']) != 0:
            any_new = True

        if len(threads[board]['current']) != 0:
            message += f"---/{board}/---\n"
            message += "Current: \n"
            message += threads_to_str(threads[board]['current'], punctuator='-')
        if len(threads[board]['new']) != 0:
            message += "New: \n"
            message += threads_to_str(threads[board]['new'], punctuator='-')

    print(message)

    if not send_only_if_new:
        send_notification(title, message)
        print("Sent notification")
    elif send_only_if_new and any_new:
        send_notification(title, message)
        print("Sent notification")
    else:
        print("Didn't send anything")


check_boards(send_only_if_new=False)
