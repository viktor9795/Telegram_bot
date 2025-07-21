import telebot
import requests
import subprocess
import sys
import os
import pandas as pd
import json
from datetime import datetime, timedelta
import openpyxl

ROOT_DIR = r'/Users/viktorgreznow/Desktop/Telegram_bot_for_sailing_scool'
bot = telebot.TeleBot(BOT_ID)


def weekle_events_search(company_id, token, url)-> None:
    auth = f'Bearer {token}'
    current_time = datetime.now()
    current_date = current_time.date()
    new_date = current_date + timedelta(weeks=2)
    params = {'from' : str(current_date), 'till' : str(new_date)}
    headers = {'Authorization' : auth, 'company_id' : company_id, 'Accept' : 'application/vnd.yclients.v2+json',
               'Content-Type' : 'application/json'}
    respone = requests.get(url=url, params= params, headers=headers)
    if respone.status_code == 200:
        output = respone.json()
        with open('events.json', 'w', encoding='utf-8') as f:
            json.dump(output['data'], f, ensure_ascii=False, indent=4)
    else:
        print(respone.status_code)

    return None

def json_to_data(path_to_json):
    data = pd.DataFrame(columns=['дата', 'тренер', 'название_события', 'комментарий'])
    with open('events.json', 'r', encoding='utf-8') as f:
        for n, event in enumerate(json.load(f)):
            print(n, event)
            data.at[n, 'дата'] = event['date']
            data.at[n, 'тренер'] = event['staff']['name']
            data.at[n, 'название_события'] = event['service']['title']
            data.at[n, 'комментарий'] = event['service']['comment']
    data.to_excel(r'/Users/viktorgreznow/Desktop/Telegram_bot_for_sailing_scool/Telegram_bot/esults.xlsx')

if __name__ == '__main__':
    list_new_dir  = []

    for path in sys.path:
        if not path.endswith('Telegram_bot'):
            list_new_dir.append(os.path.join(ROOT_DIR, r'Telegram_bot'))
        elif not path.endswith('bot_code'):
            list_new_dir.append(os.path.join(ROOT_DIR, r'Telegram_bot/bot_code'))
        elif not path.endswith('events'):
            list_new_dir.append(os.path.join(ROOT_DIR, r'Telegram_bot/events'))
    
    for p in list_new_dir:
        sys.path.append(p)
    
    from config import BEARER_TOKEN, URL_EVENTS, COMPANY_ID, URL_GROUP_EVENTS, URL_DATE_GROUP_EVENTS, BOT_ID

    try:
        weekle_events_search(COMPANY_ID, BEARER_TOKEN, URL_EVENTS)
        json_to_data(r'/Users/viktorgreznow/Desktop/Telegram_bot_for_sailing_scool/Telegram_bot/events.json')
    except Exception as e:
        print('запуск')
        subprocess.run(['python', '-m', 'events.events'])
        weekle_events_search(COMPANY_ID, BEARER_TOKEN, URL_EVENTS)
        subprocess.run(['python', '-m', 'events.json_to_data'])
        json_to_data(r'/Users/viktorgreznow/Desktop/Telegram_bot_for_sailing_scool/Telegram_bot/events.json')