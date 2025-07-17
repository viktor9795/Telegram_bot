import telebot
import requests
from datetime import datetime, timedelta
import subprocess

from telebot import types
#from ..bot.config import BEARER_TOKEN, URL, COMPANY_ID

BEARER_TOKEN = 'xr29mr69b4k9rbmz38dm'
COMPANY_ID = '8608'

bot = telebot.TeleBot('8038575218:AAGZF_QASpCY85z540beqVRrO5dt4Y-9P34')

def weekle_events_search(company_id, token):
    auth = f'Bearer {token}'
    url = f'https://api.yclients.com/api/v1/activity/{company_id}/search/'
    current_time = datetime.now()
    current_date = current_time.date()
    new_date = current_date + timedelta(weeks=1)
    params = {'from' : current_date, 'till' : new_date}
    headers = {'Authorization' : auth, 'company_id' : company_id, 'Accept' : 'application/vnd.yclients.v2+json',
               'Content-Type' : 'application/json'}
    respone = requests.get(url=url, params= params, headers=headers)
    if respone.status_code == 200:
        print(respone.text)
    else:
        print(respone)

if __name__ == '__main__':
    try:
        weekle_events_search(COMPANY_ID, BEARER_TOKEN)
    except Exception as e:
        print('запуск')
        subprocess.run(['python', '-m', 'events.events.py'])
    