import sqlite3


def createposttable(postname):
    postname = f'{postname}'
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {postname} (
    button_id INTEGER PRIMARY KEY AUTOINCREMENT,
    button_name VARCHAR,
    button_number INTEGER DEFAULT 0,
    user_id INTEGER  UNIQUE,
    phone INTEGER UNIQUE
    )
    ''')
    database.commit()
    database.close()


def createpostdatatable():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_name VARCHAR UNIQUE,
    complete INTEGER DEFAULT 0)
    ''')
    database.commit()
    database.close()


# def  createcaptcha():
#     database = sqlite3.connect('database.sqlite')
#     cursor = database.cursor()
#     cursor.execute(f'''CREATE TABLE IF NOT EXISTS captcha (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         image BLOB,
#         value VARCHAR
#         )
#         ''')
#     database.commit()
#     database.close()


import random


def getcaptcha():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    num = random.randint(1, 100)
    print(num)
    cursor.execute('''SELECT * FROM captcha WHERE id = ?''', (num,))
    item = cursor.fetchone()
    return item


def chekctable(table_name):
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute('''SELECT complete FROM posts WHERE post_name = ?''', (table_name,))
    item = cursor.fetchone()
    return item


def stoptable(table_name):
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute(f'''SELECT complete FROM posts WHERE post_name = ?''', (table_name,))
    complete = cursor.fetchone()[0]
    complete += 1
    database.commit()
    database.close()
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute(f'''UPDATE posts SET complete = ? WHERE post_name = ?''',
                   (complete, table_name))
    database.commit()
    database.close()


# def registerusertable():
#     database = sqlite3.connect('database.sqlite')
#     cursor = database.cursor()
#     cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         fullname VARCHAR,
#         chatid INTEGER UNIQUE,
#         phone INTEGER,
#         username VARCHAR
#         )
#         ''')
#     database.commit()
#     database.close()
def registeruser(fullname, chatid, username):
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute('''SELECT chatid FROM users WHERE chatid = ?''', (chatid,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(f'''INSERT INTO users(fullname, chatid, username) VALUES(?,?,?)''', (fullname, chatid, username))
        database.commit()
        database.close()
    else:
        pass


def getusers():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute('''SELECT chatid FROM users''' )
    users = cursor.fetchall()

    database.commit()
    database.close()

    return users