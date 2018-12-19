from flask import Flask, request
from pymessenger.bot import Bot
import os
import requests


app = Flask(__name__)
bot = Bot(os.environ['ACCESS_TOKEN'])

# Dealing with GET method for verification


@app.route('/', methods=['GET', ])
def hanlde_verification():
    print('Access token: ', os.environ['ACCESS_TOKEN'])
    print('Verify token: ', os.environ['VERIFY_TOKEN'])
    print('Request token: ', request.args.get('hub.verify_token', ''))
    print('Equals?: ', str(request.args.get(
        'hub.verify_token', '')) == str(os.environ['VERIFY_TOKEN']))
    if request.args.get('hub.verify_token', '') == os.environ['VERIFY_TOKEN']:
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
