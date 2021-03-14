import requests

from setup import config

app_token = config['PUSHOVER_APP_TOKEN']
user_key = config['PUSHOVER_USER_KEY']

api_endpoint = 'https://api.pushover.net/1/messages.json'


def send_notification(title, message) -> requests.Response:
    parameters = {
        'token': app_token,
        'user': user_key,
        'message': message,
        'title': title
    }

    response = requests.post(api_endpoint, parameters)
    return response
