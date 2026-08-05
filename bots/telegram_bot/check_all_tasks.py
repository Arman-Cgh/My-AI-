from database.db import get_connection, init_db


init_db()


conn = get_connection()
cursor = conn.cursor()


cursor.execute(
    """
    SELECT
        id,
        user_id,
        title,
        due_date,
        status
    FROM tasks
    """
)


rows = cursor.fetchall()


for row in rows:
    print(row)


conn.close()