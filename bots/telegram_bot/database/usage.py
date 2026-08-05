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

def get_usage(user_id):
    """Return usage dict for today for the given user."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            messages,
            images,
            code_requests,
            searches
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
            "code_requests": 0,
            "searches": 0
        }

    return {
        "messages": row[0],
        "images": row[1],
        "code_requests": row[2],
        "searches": row[3]
    }


# ==========================
# Add Usage
# ==========================

def add_usage(user_id, feature, amount=1):
    """Increment usage for a feature. Supported features: 'chat', 'image', 'technical', 'vision'.

    This function only handles storage. Permission checks must be done elsewhere.
    """
    FEATURE_COLUMN_MAP = {
        "chat": "messages",
        "image": "images",
        "technical": "code_requests",
        "vision": "searches"
    }

    if feature not in FEATURE_COLUMN_MAP:
        raise ValueError("Unknown feature")

    column = FEATURE_COLUMN_MAP[feature]

    conn = get_connection()
    cursor = conn.cursor()

    today = get_today()

    # check if a row exists
    cursor.execute(
        "SELECT 1 FROM usage WHERE user_id=? AND date=?",
        (user_id, today)
    )
    exists = cursor.fetchone()

    if not exists:
        # insert a new row with zeros except the column to increment
        msgs = 0
        imgs = 0
        codes = 0
        searches = 0

        if column == "messages":
            msgs = amount
        elif column == "images":
            imgs = amount
        elif column == "code_requests":
            codes = amount
        elif column == "searches":
            searches = amount

        cursor.execute(
            """
            INSERT INTO usage (user_id, date, messages, images, code_requests, searches)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                today,
                msgs,
                imgs,
                codes,
                searches
            )
        )

    else:
        # update existing row
        cursor.execute(
            f"UPDATE usage SET {column} = {column} + ? WHERE user_id=? AND date=?",
            (amount, user_id, today)
        )

    conn.commit()
    conn.close()
    return True


# ==========================
# Check and Increment (atomic)
# ==========================

def check_and_increment_usage(user_id, feature, limit, amount=1):
    """Atomically check current usage + amount <= limit and increment if allowed.

    Uses SQLite transaction with BEGIN IMMEDIATE to reduce race conditions.
    Returns True if incremented, False if limit would be exceeded.
    """
    FEATURE_COLUMN_MAP = {
        "chat": "messages",
        "image": "images",
        "technical": "code_requests",
        "vision": "searches"
    }

    if feature not in FEATURE_COLUMN_MAP:
        raise ValueError("Unknown feature")

    column = FEATURE_COLUMN_MAP[feature]
    today = get_today()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Acquire a write lock to serialize writers
        cursor.execute("BEGIN IMMEDIATE")

        # Ensure row exists
        cursor.execute(
            "SELECT messages, images, code_requests, searches FROM usage WHERE user_id=? AND date=?",
            (user_id, today)
        )
        row = cursor.fetchone()

        if not row:
            # insert zero row first
            cursor.execute(
                "INSERT INTO usage (user_id, date, messages, images, code_requests, searches) VALUES (?, ?, 0, 0, 0, 0)",
                (user_id, today)
            )
            current = 0
        else:
            col_index = {
                'messages': 0,
                'images': 1,
                'code_requests': 2,
                'searches': 3
            }[column]
            current = row[col_index] or 0

        # check limit
        if current + amount <= int(limit):
            # perform update
            cursor.execute(
                f"UPDATE usage SET {column} = {column} + ? WHERE user_id=? AND date=?",
                (amount, user_id, today)
            )
            conn.commit()
            return True
        else:
            conn.rollback()
            return False
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass

