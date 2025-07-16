import pandas as pd
import sqlite3

connection = sqlite3.connect('base.sql')

df = pd.read_sql("""SELECT * FROM users;""", connection)
print(df)

df_2 = pd.read_sql("""SELECT * FROM autorize_users;""", connection)
print(df_2)

df_3 = pd.read_sql("""SELECT * FROM users_feedback;""", connection)
print(df_3)