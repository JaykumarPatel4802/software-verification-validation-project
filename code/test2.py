import sqlite3

conn = sqlite3.connect("database/Chinook_Sqlite.sqlite")
cur = conn.cursor()

cur.execute("SELECT COUNT(AlbumId) as artists_count, COUNT(CustomerId) as customers_count FROM Album UNION ALL SELECT COUNT(ArtistId), 0 FROM Customer")
rows = cur.fetchall()
print(rows)

conn.close()