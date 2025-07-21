import requests
from config import BEARER_TOKEN, URL
import sqlite3
from datetime import datetime


def auth_user(login: str, password: str, id_telegramm, url: str):
    headers = {"Authorization" : f"Bearer {BEARER_TOKEN}", 
               "Accept" : "application/vnd.yclients.v2+json", 
               "Content-Type" : "application/json"}
    data= {
    "login" : login,
    "password": password
    }
    full_response = requests.post(url, headers= headers, json= data)
    response = full_response.json()
    if full_response.status_code == 201 and response["data"]["is_approved"] == True:
        curr_time = datetime.now()
        user_token = response["data"]["user_token"]
        name = response["data"]["name"]
        user_id = response["data"]["id"]
        phone = response["data"]["phone"]
        conn = sqlite3.connect('base.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS autorize_users (id_telegramm int auto_increment prymary key, user_id int, name varchar(50), user_token varchar(50), phone int, date date, time time)')
        cur.execute("INSERT INTO autorize_users (id_telegramm, user_id, name, user_token, phone, date, time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (id_telegramm, user_id, name, user_token, phone, curr_time.date(), curr_time.time()))
        conn.commit()
        cur.close()
        conn.close()
        return "Вы успешно авторизовались"
    else:
        return "Что-то не так с авторизацией"



def user_book(user_token):
    url = 'https://api.yclients.com/api/v1/user/records/{record_id}/{record_hash}'
    pass