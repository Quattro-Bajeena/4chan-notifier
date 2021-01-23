import requests

APP_TOKEN = 'akdk1y8ckyu8xj5ydom48auqb5zptd'
USER_KEY = 'uc3u2h6j9r3pidhtm67e8mt3frzs1t'
api_endpoint = 'https://api.pushover.net/1/messages.json'


def send_notification(title, message) -> requests.Response:
    parameters = {
        'token': APP_TOKEN,
        'user': USER_KEY,
        'message': message,
        'title': title
    }

    response = requests.post(api_endpoint, parameters)
    return response
