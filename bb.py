import requests
import telegram
import os
import sys
from dotenv import load_dotenv
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
        data = response.json()
        ss = data['new_attempts'][0]['lesson_title']
        if data['new_attempts'][0]['is_negative']:
            bot.send_message(chat_id=sys.argv[1],
                             text=f"У вас проверили работу {ss}. К сожалению, в работе нашлись ошибки.")
        else:
            bot.send_message(chat_id=sys.argv[0],
                             text=f"У вас проверили работу {ss}. Преподавателю все понравилось, можно приступать к следующему уроку!")
        print(response.json())
        payload['timestamp'] = response.json()['last_attempt_timestamp']
    except requests.exceptions.ReadTimeout:
        print("ReadTimeout")
    except requests.exceptions.ConnectionError:
        print("ConnectionError")

