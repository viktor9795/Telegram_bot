import telebot

from reqest_to_yacl import auth_user

bot = telebot.TeleBot('8038575218:AAGZF_QASpCY85z540beqVRrO5dt4Y-9P34')
user_auth_info = {}


def authorization_login(message):
    login = message.text
    user_auth_info['login'] = str(login)
    bot.send_message(message.chat.id, 'Вам необходимо авторизоваться в системе, перейдем к паролю, введите пароль:')
    bot.register_next_step_handler(message, authorization_password)

def authorization_password(message):
    passwod = message.text
    user_auth_info['password'] = str(passwod)
    result = auth_user(user_auth_info['login'], user_auth_info['password'], message.from_user.id)
    if result == "Вы успешно авторизовались":
        pass
    elif result == "Что-то не так с авторизацией":
        marckup_2 = types.InlineKeyboardMarkup()
        btn_6 = types.InlineKeyboardButton("Пройти \n регистрацию", url= 'https://n1412178.yclients.com/')
        btn_7 = types.InlineKeyboardButton("Попробовать снова", callback_data= 'start')
        marckup_2.row(btn_6)
        marckup_2.row(btn_7)
        bot.send_message(message.chat.id, "Пройдите регистрацию в ситсеме", reply_markup= marckup_2)