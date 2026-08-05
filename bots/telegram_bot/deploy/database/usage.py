from datetime import datetime

from database.db import get_connection



# ==========================
# Get Today
# ==========================

def get_today():

    return datetime.now().date().isoformat()



# ==========================
# Get User Usage Today
# ==========================

def get_usage(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        messages,
        images,
        code_requests

        FROM usage

        WHERE user_id=?

        AND date=?

        """,
        (
            user_id,
            get_today()
        )
    )


    row = cursor.fetchone()

    conn.close()


    if not row:

        return {

            "messages": 0,

            "images": 0,

            "code_requests": 0

        }


    return {

        "messages": row[0],

        "images": row[1],

        "code_requests": row[2]

    }



# ==========================
# Add Message Usage
# ==========================

def add_message_usage(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    today = get_today()


    usage = get_usage(
        user_id
    )


    if usage["messages"] == 0:

        cursor.execute(
            """
            INSERT INTO usage
            (
                user_id,
                date,
                messages
            )

            VALUES(?,?,1)

            """,
            (
                user_id,
                today
            )
        )


    else:

        cursor.execute(
            """
            UPDATE usage

            SET messages = messages + 1

            WHERE user_id=?

            AND date=?

            """,
            (
                user_id,
                today
            )
        )


    conn.commit()
    conn.close()



# ==========================
# Check Message Limit
# ==========================

def can_send_message(
    user_id,
    daily_limit
):

    usage = get_usage(
        user_id
    )


    if usage["messages"] >= daily_limit:

        return False


    return True


# ==========================
# Image Usage
# ==========================

def can_send_image(
    user_id,
    daily_limit
):

    usage = get_usage(
        user_id
    )


    if usage["images"] >= daily_limit:

        return False


    return True


# ==========================
# Technical Question Usage
# ==========================

def can_send_technical_question(
    user_id,
    daily_limit
):

    usage = get_usage(
        user_id
    )


    if usage["code_requests"] >= daily_limit:

        return False


    return True