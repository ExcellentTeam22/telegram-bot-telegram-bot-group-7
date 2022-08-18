from flask import Flask, request, Response
import requests
from sympy import isprime

TOKEN = '5540736039:AAEEhq0rWfMMt8xyUUBoxF_Zd4xWTeCryFQ'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://79c3-82-80-173-170.eu.ngrok.io/message'.format(TOKEN)


app = Flask(__name__)


@app.route('/sanity')
def sanity():
    return "Server is running"


def is_even(n: int):
    if n % 2 == 0:
        return True
    return False


def is_prime(n: int):
    return isprime(n)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    input = request.get_json()['message']['text']
    chat_id = request.get_json()['message']['chat']['id']

    if input.split(" ")[0] != '/prime':
        message_to_send = "don't know this command, try again"
    elif len(input.split(" ")) == 2:
        number = input.split(" ")[1]
        if not number.isnumeric():
            message_to_send = "I'm working just with numbers"
        else:
            number = int(number)
            if is_even(number) and not input == 2:
                message_to_send = "Come on dude, you know even numbers are not prime!"
            elif is_prime(number):
                message_to_send = "prime"
            else:
                message_to_send = "not prime"
    else:
        message_to_send = "enter the number you want to check after the '/prime'"

    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, message_to_send))
    return Response("success")


if __name__ == '__main__':
    response = requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002)
