import sqlite3

def createposttable(postname):
    postname = f'{postname}'
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {postname} (
    button_id INTEGER PRIMARY KEY AUTOINCREMENT,
    button_name VARCHAR,
    button_number INTEGER DEFAULT 0,
    user_id INTEGER  UNIQUE
    )
    ''')
    database.commit()
    database.close()

