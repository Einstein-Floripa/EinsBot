from flask import Flask, request
from sensitive import VERIFY_TOKEN, ACCESS_TOKEN
from pymessenger.bot import Bot
import requests


app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

# Dealing with GET method for verification


@app.route('/', methods=['GET', ])
def hanlde_verification():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', '')

    else:
        return 'Error, wrong verification token'


# Dealing with POST method for messaging
@app.route('/', methods=['POST', ])
def handle_message():
    input_data = request.get_json()

    for event in input_data['entry']:
        messaging = event['messaging']
        for message in messaging:
            recipient_id = message['sender']['id']

            send_message(recipient_id, get_response_message())


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)


def get_response_message():
    return ('Hello!')


if __name__ == '__main__':
    app.run()
