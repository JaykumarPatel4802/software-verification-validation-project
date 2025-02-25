import sqlite3

with sqlite3.connect('database/chinook.db') as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM albums")

    rows = cursor.fetchall()

    for row in rows:
        print(row)
