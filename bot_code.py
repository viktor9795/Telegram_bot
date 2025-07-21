import telebot
from telebot import types
import webbrowser
import sqlite3
import datetime
import sys
import os
import subprocess


ROOT_DIR = r'/Users/viktorgreznow/Desktop/Telegram_bot_for_sailing_scool'
bot = telebot.TeleBot(BOT_ID)


@bot.message_handler(commands = ['start'])
def function_start(message):
    name = message.from_user.first_name
    id = message.from_user.id
    datestamp = datetime.datetime.now().date()
    timestamp = datetime.datetime.now().time()
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id_telegramm int auto_increment prymary key, name varchar(50), date date, time time)')
    cur.execute("INSERT INTO users (id_telegramm, name, date, time) VALUES ('%s', '%s', '%s', '%s')" % (id, name, datestamp, timestamp))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton('Записаться на тернировку')
    btn_2 = types.KeyboardButton('Календарь мероприятий')
    btn_3 = types.KeyboardButton('Подключить информирование')
    btn_4 = types.KeyboardButton('Арендовать луч')
    btn_5 = types.KeyboardButton('Оставить отзыв')
    markup.row(btn_1)
    markup.row(btn_2, btn_3)
    markup.row(btn_4, btn_5)
    bot.send_message(message.chat.id, f'Привет, {name if name is not None else 'яхтсмен'}!', reply_markup= markup)
    bot.register_next_step_handler(message, on_start_button_click)

def on_start_button_click(message):
    if message.text == 'Записаться на тернировку':
        webbrowser.open('http://overlapped.ru')
    elif message.text == 'Календарь мероприятий':
        bot.send_message(message.chat.id, 'расписание мероприятий')
    elif message.text == 'Подключить информирование':
        bot.send_message(message.chat.id, 'Вам необходимо авторизоваться в системе, начнем с логина, введите логин:')
        bot.register_next_step_handler(message, authorization_login)
    elif message.text == 'Арендовать луч':
        bot.send_message(message.chat.id, text_message_rent_laser(message.from_user.first_name))
    elif message.text == 'Оставить отзыв':
        bot.send_message(message.chat.id, 'Напишите свой отзыв в сообщении и отправте его')
        bot.register_next_step_handler(message, feedback_func)

        
def feedback_func(message):
    bot.send_message(message.chat.id, feedback(str(message.text), message.from_user.id, message.from_user.first_name))



@bot.message_handler(commands = ['help'])
def function_help(message):
    bot.send_message(message.chat.id, "Список команд и их описание: \n/start - запускает бота \n/site - ознакомиться с сайтом", parse_mode= 'html')


@bot.message_handler(commands = ['site'])
def function_open_site(message):
    webbrowser.open('http://overlapped.ru')


@bot.message_handler()
def users_response(message):
    if message.text:
        bot.send_message(message.chat.id, 'Нажмите на команду, либо введите вместо сообщения: /help')

"""@bot.callback_query_handler(func= lambda get_race_info: True)
def get_race_info(race_info):
    pass"""

@bot.callback_query_handler(func= lambda callback: True)
def open_yacl(callback):
    if callback.data == 'start':
        bot.send_message(callback.message.chat.id, 'Вам необходимо авторизоваться в системе, начнем с логина, введите логин:')
        bot.register_next_step_handler(callback.message, authorization_login)


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
    
    from bot.reqest_to_yacl import auth_user
    from bot.rent_laser import rent_laser, text_message_rent_laser
    from bot.feedback import feedback
    from bot.autorization import authorization_login, authorization_password
    from config import BOT_ID
    subprocess.run(['python', '-m', 'bot_code'])
    bot.polling(non_stop= True)
