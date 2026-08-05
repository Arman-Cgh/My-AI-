import sqlite3

conn = sqlite3.connect("database/users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM messages")

for row in cursor.fetchall():
    print(row)

conn.close()