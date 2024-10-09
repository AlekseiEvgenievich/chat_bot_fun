import requests
import telegram
import os
import sys
import time
from dotenv import load_dotenv


def main():
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        "Authorization": os.environ['DEVMAN_TOKEN']}
    payload = {}

    while True:
        try:
            response = requests.get(url, headers=headers, params=payload,
                                    timeout=10)
            response.raise_for_status()
            bot = telegram.Bot(
                token=os.environ['TELEGRAM_TOKEN'])
            json_response = response.json()
            lesson_name = json_response['new_attempts'][0]['lesson_title']
            if json_response['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=sys.argv[1],
                                 text=f"У вас проверили работу {lesson_name}. К сожалению, в работе нашлись ошибки.")
            else:
                bot.send_message(chat_id=sys.argv[0],
                                 text=f"У вас проверили работу {lesson_name}. Преподавателю все понравилось, можно приступать к следующему уроку!")
            payload['timestamp'] = response.json()['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(200)

if __name__ == '__main__':
    main()
