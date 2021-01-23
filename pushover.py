import requests
import os
from dotenv import load_dotenv
load_dotenv()

APP_TOKEN = os.getenv('PUSHOVER_APP_TOKEN')
USER_KEY = os.getenv('PUSHOVER_USER_KEY')

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
