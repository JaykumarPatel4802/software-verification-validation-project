import sqlite3

class SQLiteHelper:

    def __init__(self):
        self.conn = sqlite3.connect("database/Chinook_Sqlite.sqlite")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def executeQuery(self, query):
        print("Executing Query:")
        print(query)
        try:
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows, None  # Return rows and None for no error
        except sqlite3.Error as e:
        # except Exception as e:
            return None, str(e)  # Return None for rows and the error message