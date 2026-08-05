from database.db import get_connection


def get_bot_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages")
    messages = cursor.fetchone()[0]

    conn.close()

    return users, messages