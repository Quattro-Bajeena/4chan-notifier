from datetime import timedelta

from parse_board_data import get_threads, filter_threads, threads_to_str
from setup import boards, endpoints, data_path, searched_words, config
from get_board_data import download_threads_time_check
from pushover import send_notification


def check_boards(send_only_if_new: bool, check_comment = False, minute_threshold : float = 1, debug_mode : bool = False):
    download_threads_time_check(boards, endpoints, timedelta(minutes=minute_threshold))

    threads = get_threads(boards, data_path)
    title = "Current threads with searched words"
    message = ''

    any_new = False
    for board in threads:
        threads[board]['current'] = filter_threads(threads[board]['current'], searched_words, check_comment=check_comment)
        threads[board]['new'] = filter_threads(threads[board]['new'], searched_words, check_comment=check_comment)

        if len(threads[board]['new']) != 0:
            any_new = True

        message += f"---/{board}/---\n"
        if len(threads[board]['current']) != 0:
            message += "Current: \n"
            message += threads_to_str(threads[board]['current'], punctuator='-')
        if len(threads[board]['new']) != 0:
            message += "New: \n"
            message += threads_to_str(threads[board]['new'], punctuator='-')

    print("MESSAGE:")
    print(title)
    print(message)

    # debug mode - not sending the message
    if debug_mode:
        print("DEBUG MODE - didint sent message")
        return
    if not send_only_if_new:
        send_notification(title, message)
        print("Sent notification")
    elif send_only_if_new and any_new:
        send_notification(title, message)
        print("There is a new thread - Sent notification")
    else:
        print("Didn't send anything")


if __name__ == '__main__':

    check_boards(
        send_only_if_new=config['SEND_ONLY_IF_NEW'],
        check_comment=config['CHECK_COMMENT'],
        minute_threshold=config['MINUTE_THRESHOLD'], 
        debug_mode=config['DEBUG_MODE']
    )
