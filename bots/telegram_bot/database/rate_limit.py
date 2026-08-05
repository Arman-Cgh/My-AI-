import time

from database.db import get_connection


def get_last_message_time(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT last_message
        FROM rate_limits
        WHERE user_id = ?
        """,
        (user_id,)
    )


    result = cursor.fetchone()

    conn.close()


    if result:
        return result[0]


    return None



def update_last_message_time(user_id: int):

    now = time.time()


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO rate_limits
        (
            user_id,
            last_message
        )
        VALUES (?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
        last_message = excluded.last_message

        """,
        (
            user_id,
            now
        )
    )


    conn.commit()
    conn.close()


    return now