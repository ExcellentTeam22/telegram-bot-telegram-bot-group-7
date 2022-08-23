from typing import List

from flask import Flask, request, Response
import requests
import api_rhyme


TOKEN = '5540736039:AAEEhq0rWfMMt8xyUUBoxF_Zd4xWTeCryFQ'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://79c3-82-80-173-170.eu.ngrok.io/message'.format(TOKEN)
CHAT_ID = 299020284
USER_WORD = ""
START_STATE = True

app = Flask(__name__)

def order_the_words(words: List) -> str:
    words_list = ""
    for i in words:
        words_list += i + '\n'
    return words_list


def get_rhyme(word: str, number: int = 5) -> str:
    words = api_rhyme.give_rhymes(word)
    if not words:
        return "מצטערים, לא מצאנו חרוז למילה שחיפשתם😮"
    return order_the_words(words[:number])


def handle_rhyme(user_input: str, number: str, chat_id: int):
    if number == '*':
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "לא בחרתם מספר, חמישה חרוזים יוצגו למילה " + user_input[0] + ":"))
        message_to_send = get_rhyme(word=user_input[0])
    else:
        if len(user_input) == 0:
            message_to_send = "לא בחרתם מילה לחרוז, ניתן ללחוץ על עזרה כדי להתקדם"
        else:
            number = int(number)
            word = user_input[-1]
            message_to_send = get_rhyme(word=word, number=number)
    return message_to_send


def get_number(chat_id: int):
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, "אנא בחרו מספר חרוזים שיוצגו,\n אם אינכם מעוניינים לבחור מספר לחצו על *"))

def handle_help():
    # send option to the user
    pass


@app.route('/message', methods=["POST"])
def handle_message():
    global START_STATE
    global USER_WORD
    print("got message")
    if 'message' in request.get_json():
        user_input = request.get_json()['message']['text']
        chat_id = request.get_json()['message']['chat']['id']
        command = user_input.split()[0]
        if START_STATE:
            match command:
                case '/start':
                    message_to_send = "שלום לכם😊\nאני בוט חרוזים\nהקלידו את המילה חרוז ולאחר מכן את המילה עבורה תרצו חרוז.\nתהנו!"
                    START_STATE = True
                    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                       .format(TOKEN, chat_id, message_to_send))
                case 'חרוז':
                    get_number(chat_id)
                    START_STATE = False
                    USER_WORD = user_input.split()[1:]

                    #message_to_send = "la la"

                case 'עזרה':
                    message_to_send = 'כדי להציג חרוזים, יש להקליד בפורמט הבא:\n' \
                                      'חרוז   --מילה לחרוז--'
                    START_STATE = True
                    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                       .format(TOKEN, chat_id, message_to_send))
                case 'תפריט':
                    message_to_send = ''
                case 'שלום':
                    message_to_send = "שלום גם לכם!😊\nאני בוט חרוזים, הקלידו את המילה חרוז ולאחר מכן את המילה עבורה תרצו חרוז\nתהנו!"
                    START_STATE = True
                    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                       .format(TOKEN, chat_id, message_to_send))
                case _:
                    message_to_send = "אני לא מכיר את הפקודה הזו🤨\nניתן ללחוץ על עזרה כדי להתקדם"
                    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                               .format(TOKEN, chat_id, message_to_send))
        else:
            START_STATE = True
            if user_input.isnumeric() or user_input == '*':
                message_to_send = handle_rhyme(USER_WORD, user_input, chat_id)
            else:
                message_to_send = "המספר שבחרתם לא תקין, ניתן לבחור עזרה בשביל להתקדם"
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, message_to_send))
    return Response("success")


if __name__ == '__main__':
    # response = requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002)
