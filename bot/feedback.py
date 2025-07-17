import sqlite3
from datetime import datetime

def feedback(feedback: str, id_telegramm, name):
    if not (feedback and feedback.isspace()):
        stamp = datetime.now()
        conn = sqlite3.connect('base.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users_feedback (id_telegramm int auto_increment prymary key, name varchar(50), date date, time time, feedback varchar(500))')
        cur.execute("INSERT INTO users_feedback (id_telegramm, name, date, time, feedback) VALUES ('%s', '%s', '%s', '%s', '%s')" % (id_telegramm, name, stamp.date(), stamp.time(), feedback))
        conn.commit()
        cur.close()
        conn.close()
        return "Отзыв получен, спасибо за обратную связь"
    else:
        return "Отзыв не получится отправить"