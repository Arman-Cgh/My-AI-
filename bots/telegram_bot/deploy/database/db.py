import sqlite3
import json
import os
import re
from datetime import datetime

from config import BOT_USERNAME


DB_NAME = "database/users.db"



# ==========================
# Connection
# ==========================

def get_connection():

    os.makedirs(
        "database",
        exist_ok=True
    )

    return sqlite3.connect(
        DB_NAME
    )



# ==========================
# Initialize Database
# ==========================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()


    # ======================
    # Users
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY,

        username TEXT DEFAULT '',

        first_name TEXT DEFAULT '',

        nickname TEXT DEFAULT '',

        bio TEXT DEFAULT '',

        interests TEXT DEFAULT '',

        plan TEXT DEFAULT 'free'

    )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rate_limits
        (
            user_id INTEGER PRIMARY KEY,

            last_message REAL

        )
        """)



    # ======================
    # Messages
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        role TEXT,

        message TEXT

    )
    """)



    # ======================
    # Memory
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        memory_key TEXT NOT NULL,

        memory_value TEXT,

        UNIQUE(user_id,memory_key)

    )
    """)



    # ======================
    # Question cache
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qa_cache(

       id INTEGER PRIMARY KEY AUTOINCREMENT,

       user_id INTEGER,

       question TEXT,

       normalized_question TEXT,

       answer TEXT,

       UNIQUE(user_id, normalized_question)

    )
    """)



    # ======================
    # State
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_state(

        user_id INTEGER PRIMARY KEY,

        active_project TEXT DEFAULT '',

        current_goal TEXT DEFAULT '',

        preferences TEXT DEFAULT '{}'

    )
    """)



    # ======================
    # Plans
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plans(
 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        name TEXT UNIQUE,
 
        daily_messages INTEGER DEFAULT 30,
 
        daily_images INTEGER DEFAULT 2,
 
        daily_technical_questions INTEGER DEFAULT 3,
 
        cooldown_seconds INTEGER DEFAULT 5
 
    )
    """)

    cursor.execute("PRAGMA table_info(plans)")
    plan_columns = [row[1] for row in cursor.fetchall()]
    if "daily_technical_questions" not in plan_columns:
       cursor.execute("ALTER TABLE plans ADD COLUMN daily_technical_questions INTEGER DEFAULT 3")

    cursor.execute(
       """
       INSERT OR IGNORE INTO plans
 
        (
            name,
            daily_messages,
            daily_images,
            daily_technical_questions,
            cooldown_seconds
        )
 
        VALUES
 
        ('free',30,1,3,5),
 
        ('pro',1000,2,10,1),
 
        ('ultra',999999,4,99999,0)
 
        """
    )

    cursor.execute(
       """
       UPDATE plans
       SET daily_technical_questions = CASE
           WHEN name='free' THEN 3
           WHEN name='pro' THEN 10
           WHEN name='ultra' THEN 99999
           ELSE daily_technical_questions
       END,
       daily_images = CASE
           WHEN name='free' THEN 1
           WHEN name='pro' THEN 2
           WHEN name='ultra' THEN 4
           ELSE daily_images
       END,
       daily_messages = CASE
           WHEN name='free' THEN 30
           WHEN name='pro' THEN 1000
           WHEN name='ultra' THEN 999999
           ELSE daily_messages
       END,
       cooldown_seconds = CASE
           WHEN name='free' THEN 5
           WHEN name='pro' THEN 1
           WHEN name='ultra' THEN 0
           ELSE cooldown_seconds
       END
       WHERE name IN ('free','pro','ultra')
       """
    )

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plan_prices(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       plan_name TEXT UNIQUE,
       duration_days INTEGER DEFAULT 30,
       price INTEGER DEFAULT 0,
       currency TEXT DEFAULT 'IRR',
       is_active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_requests(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER,
       plan_name TEXT,
       duration_days INTEGER DEFAULT 30,
       amount INTEGER DEFAULT 0,
       currency TEXT DEFAULT 'IRR',
       gateway TEXT DEFAULT 'placeholder',
       gateway_reference TEXT DEFAULT '',
       status TEXT DEFAULT 'pending',
       created_at TEXT DEFAULT ''
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS referral_settings(
       id INTEGER PRIMARY KEY CHECK (id = 1),
       required_invites INTEGER DEFAULT 3,
       reward_days INTEGER DEFAULT 3,
       reward_plan TEXT DEFAULT 'pro'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS referrals(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       inviter_id INTEGER,
       invited_id INTEGER,
       reward_given INTEGER DEFAULT 0,
       created_at TEXT DEFAULT ''
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO plan_prices(plan_name, duration_days, price, currency, is_active)
    VALUES
       ('free', 30, 0, 'IRR', 1),
       ('pro', 30, 300000, 'IRR', 1),
       ('ultra', 30, 700000, 'IRR', 1)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO referral_settings(id, required_invites, reward_days, reward_plan)
    VALUES (1, 3, 3, 'pro')
    """)



    # ======================
    # Usage
    # ======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usage(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        date TEXT,

        messages INTEGER DEFAULT 0,

        images INTEGER DEFAULT 0,

        code_requests INTEGER DEFAULT 0,

        searches INTEGER DEFAULT 0,

        UNIQUE(user_id,date)

    )
    """)



    # ======================
    # Subscription
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE,

        plan TEXT DEFAULT 'free',

        start_date TEXT,

        duration_days INTEGER DEFAULT 0,

        status TEXT DEFAULT 'inactive'

    )
    """)

    # Upgrade old subscriptions schema if needed
    cursor.execute("PRAGMA table_info(subscriptions)")
    columns = [row[1] for row in cursor.fetchall()]
    if "plan" not in columns:
        cursor.execute("ALTER TABLE subscriptions RENAME TO subscriptions_old")
        cursor.execute("""
        CREATE TABLE subscriptions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            plan TEXT DEFAULT 'free',
            start_date TEXT,
            duration_days INTEGER DEFAULT 0,
            status TEXT DEFAULT 'inactive'
        )
        """)
        today = datetime.now().date().isoformat()
        cursor.execute(
            """
            INSERT INTO subscriptions(user_id, plan, start_date, duration_days, status)
            SELECT
                user_id,
                COALESCE((SELECT name FROM plans WHERE id = subscriptions_old.plan_id), 'free'),
                '',
                0,
                CASE
                    WHEN expire_date > ? THEN 'active'
                    ELSE 'expired'
                END
            FROM subscriptions_old
            """,
            (
                today,
            )
        )
        cursor.execute("DROP TABLE subscriptions_old")



    # ======================
    # Ban list
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banned_users(

       user_id INTEGER PRIMARY KEY,

       reason TEXT DEFAULT '',

       banned_at TEXT DEFAULT ''

    )
    """)


    # ======================
    # Rate Limit
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rate_limit(
 
        user_id INTEGER PRIMARY KEY,
 
        last_request REAL DEFAULT 0
 
    )
    """)



    conn.commit()
    conn.close()



# ==========================
# Helpers
# ==========================

def normalize_text(text):

    return " ".join(
        str(text or "").strip().lower().split()
    )


# ==========================
# Cache
# ==========================


def get_cached_answer(
    user_id,
    question
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT answer

        FROM qa_cache

        WHERE user_id=?

        AND normalized_question=?

        """,
        (
            user_id,
            normalize_text(question)
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None



def save_cached_answer(
    user_id,
    question,
    answer
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO qa_cache

        (
            user_id,
            question,
            normalized_question,
            answer
        )

        VALUES(?,?,?,?)

        ON CONFLICT(user_id, normalized_question)

        DO UPDATE SET

        question=excluded.question,
        answer=excluded.answer

        """,
        (
            user_id,
            question,
            normalize_text(question),
            answer
        )
    )

    conn.commit()
    conn.close()


# ==========================
# Users
# ==========================


def add_user(
    user_id,
    username="",
    first_name=""
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR IGNORE INTO users

        (
            id,
            username,
            first_name
        )

        VALUES(?,?,?)

        """,
        (
            user_id,
            username or "",
            first_name or ""
        )
    )


    conn.commit()
    conn.close()




def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id FROM users
        """
    )


    users = [
        row[0]
        for row in cursor.fetchall()
    ]


    conn.close()


    return users



def get_all_users_info(
    limit=20
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id, username, first_name, plan

        FROM users

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            limit,
        )
    )


    rows = cursor.fetchall()

    conn.close()

    return rows



def get_user_info(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id, username, first_name, nickname, bio, interests, plan

        FROM users

        WHERE id=?
        """,
        (
            user_id,
        )
    )


    row = cursor.fetchone()

    conn.close()

    return row



def get_user_message_count(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM messages

        WHERE user_id=?
        """,
        (
            user_id,
        )
    )


    count = cursor.fetchone()[0]

    conn.close()

    return count



def get_user_message_history(
    user_id,
    limit=5
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT role, message

        FROM messages

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )


    rows = cursor.fetchall()

    conn.close()

    return rows[::-1]



def get_plan_counts():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT plan, COUNT(*)

        FROM users

        GROUP BY plan
        """
    )


    rows = cursor.fetchall()

    conn.close()

    return {
        row[0]: row[1]
        for row in rows
    }



def get_active_subscription_count():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM subscriptions

        WHERE status='active'
        """
    )


    count = cursor.fetchone()[0]

    conn.close()

    return count


def _parse_price_value(value):

    if value is None:
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(value)

    text = str(value).strip()
    if not text:
        return None

    text = text.translate(
        str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    )
    text = text.replace("٫", ".").replace("٬", "").replace("،", "")
    text = re.sub(r"(\d)/(\d)", r"\1\2", text)
    text = re.sub(r"[^\w\s.-]", " ", text)

    tokens = [token for token in re.split(r"\s+", text) if token]
    if not tokens:
        return None

    number = None

    for token in tokens:
        token_lower = token.lower()

        if token_lower in {"تومان", "toman", "t", "rial", "irr", "ریال"}:
            continue

        if token_lower in {"هزار", "k", "thousand"}:
            if number is not None:
                number *= 1000
            continue

        if token_lower in {"میلیون", "m", "million"}:
            if number is not None:
                number *= 1000000
            continue

        if token_lower in {"میلیارد", "b", "billion"}:
            if number is not None:
                number *= 1000000000
            continue

        match = re.fullmatch(r"([0-9]+)([^0-9]+)?", token)
        if match:
            parsed_value = int(match.group(1))
            unit = (match.group(2) or "").lower()
            if unit in {"هزار", "k", "thousand"}:
                parsed_value *= 1000
            elif unit in {"میلیون", "m", "million"}:
                parsed_value *= 1000000
            elif unit in {"میلیارد", "b", "billion"}:
                parsed_value *= 1000000000

            if number is None:
                number = parsed_value
            else:
                number = int(str(number) + str(parsed_value))
            continue

        try:
            parsed_value = int(float(token))
        except ValueError:
            continue

        if number is None:
            number = parsed_value
        else:
            number = int(str(number) + str(parsed_value))

    return number


def set_plan_price(plan_name, price, duration_days=30, currency="IRR"):

    normalized_price = _parse_price_value(price)
    if normalized_price is None:
        raise ValueError("price could not be parsed")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO plan_prices
        (
            plan_name,
            duration_days,
            price,
            currency,
            is_active
        )
        VALUES(?,?,?,?,1)
        ON CONFLICT(plan_name)
        DO UPDATE SET
            duration_days=excluded.duration_days,
            price=excluded.price,
            currency=excluded.currency,
            is_active=1
        """,
        (
            plan_name.lower(),
            duration_days,
            normalized_price,
            currency,
        )
    )

    conn.commit()
    conn.close()

    return normalized_price


def get_plan_price(plan_name, duration_days=30):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT price, currency, is_active
        FROM plan_prices
        WHERE plan_name=?
        AND duration_days=?
        """,
        (
            plan_name.lower(),
            duration_days,
        )
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "price": 0,
            "currency": "IRR",
            "is_active": True,
        }

    return {
        "price": row[0],
        "currency": row[1] or "IRR",
        "is_active": bool(row[2]),
    }


def get_plan_prices():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT plan_name, duration_days, price, currency, is_active
        FROM plan_prices
        ORDER BY plan_name
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return {
        row[0]: {
            "duration_days": row[1],
            "price": row[2],
            "currency": row[3] or "IRR",
            "is_active": bool(row[4]),
        }
        for row in rows
    }


def create_payment_request(user_id, plan_name, amount, currency="IRR", duration_days=30):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO payment_requests
        (
            user_id,
            plan_name,
            duration_days,
            amount,
            currency,
            gateway,
            gateway_reference,
            status,
            created_at
        )
        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (
            user_id,
            plan_name.lower(),
            duration_days,
            amount,
            currency,
            "placeholder",
            "",
            "pending",
            datetime.now().isoformat(),
        )
    )

    request_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return request_id


def get_payment_request(request_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, plan_name, duration_days, amount, currency, gateway, gateway_reference, status, created_at
        FROM payment_requests
        WHERE id=?
        """,
        (
            request_id,
        )
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "user_id": row[1],
        "plan_name": row[2],
        "duration_days": row[3],
        "amount": row[4],
        "currency": row[5],
        "gateway": row[6],
        "gateway_reference": row[7],
        "status": row[8],
        "created_at": row[9],
    }


def update_payment_request_status(request_id, status, gateway_reference=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payment_requests
        SET status=?, gateway_reference=?
        WHERE id=?
        """,
        (
            status,
            gateway_reference,
            request_id,
        )
    )

    conn.commit()
    conn.close()


def set_referral_settings(required_invites=None, reward_days=None, reward_plan=None):

    conn = get_connection()
    cursor = conn.cursor()

    if required_invites is None and reward_days is None and reward_plan is None:
        conn.close()
        return

    cursor.execute(
        """
        INSERT INTO referral_settings(id, required_invites, reward_days, reward_plan)
        VALUES(1, ?, ?, ?)
        ON CONFLICT(id)
        DO UPDATE SET
            required_invites=COALESCE(excluded.required_invites, referral_settings.required_invites),
            reward_days=COALESCE(excluded.reward_days, referral_settings.reward_days),
            reward_plan=COALESCE(excluded.reward_plan, referral_settings.reward_plan)
        """,
        (
            required_invites,
            reward_days,
            reward_plan,
        )
    )

    conn.commit()
    conn.close()


def get_referral_settings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT required_invites, reward_days, reward_plan
        FROM referral_settings
        WHERE id=1
        """
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "required_invites": 3,
            "reward_days": 3,
            "reward_plan": "pro",
        }

    return {
        "required_invites": row[0] or 3,
        "reward_days": row[1] or 3,
        "reward_plan": row[2] or "pro",
    }


def get_referral_link(user_id):

    username = (BOT_USERNAME or "").strip()
    if username:
        return f"https://t.me/{username}?start=ref_{user_id}"

    return f"https://t.me/your_bot_username?start=ref_{user_id}"


def create_referral(inviter_id, invited_id):

    if inviter_id == invited_id:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM referrals
        WHERE inviter_id=? AND invited_id=?
        """,
        (
            inviter_id,
            invited_id,
        )
    )

    exists = cursor.fetchone() is not None
    if exists:
        conn.close()
        return None

    cursor.execute(
        """
        INSERT INTO referrals
        (
            inviter_id,
            invited_id,
            reward_given,
            created_at
        )
        VALUES(?,?,0,?)
        """,
        (
            inviter_id,
            invited_id,
            datetime.now().isoformat(),
        )
    )

    conn.commit()
    conn.close()

    maybe_grant_referral_reward(inviter_id)

    return True


def maybe_grant_referral_reward(inviter_id):

    from database.subscriptions import create_subscription

    conn = get_connection()
    cursor = conn.cursor()

    settings = get_referral_settings()
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM referrals
        WHERE inviter_id=?
        """,
        (
            inviter_id,
        )
    )

    total_referrals = cursor.fetchone()[0]
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM referrals
        WHERE inviter_id=? AND reward_given=1
        """,
        (
            inviter_id,
        )
    )

    rewarded = cursor.fetchone()[0]

    conn.close()

    if total_referrals >= settings["required_invites"] and rewarded == 0:
        create_subscription(inviter_id, settings["reward_plan"], settings["reward_days"])
        update_user_plan(inviter_id, settings["reward_plan"])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE referrals
            SET reward_given=1
            WHERE inviter_id=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                inviter_id,
            )
        )
        conn.commit()
        conn.close()


def get_user_referral_stats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*), COALESCE(SUM(CASE WHEN reward_given=1 THEN 1 ELSE 0 END), 0)
        FROM referrals
        WHERE inviter_id=?
        """,
        (
            user_id,
        )
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "invites": 0,
            "rewarded": 0,
        }

    return {
        "invites": row[0] or 0,
        "rewarded": row[1] or 0,
    }


def ban_user(user_id, reason=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO banned_users
        (
            user_id,
            reason,
            banned_at
        )
        VALUES(?,?,?)
        ON CONFLICT(user_id)
        DO UPDATE SET
        reason=excluded.reason,
        banned_at=excluded.banned_at
        """,
        (
            user_id,
            reason or "",
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()



def unban_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM banned_users
        WHERE user_id=?
        """,
        (
            user_id,
        )
    )

    conn.commit()
    conn.close()



def is_user_banned(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM banned_users
        WHERE user_id=?
        """,
        (
            user_id,
        )
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists



def get_ban_reason(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT reason, banned_at
        FROM banned_users
        WHERE user_id=?
        """,
        (
            user_id,
        )
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "reason": row[0] or "",
            "banned_at": row[1] or ""
        }

    return {
        "reason": "",
        "banned_at": ""
    }



def get_profile(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        username,
        first_name,
        nickname,
        bio,
        interests

        FROM users

        WHERE id=?

        """,
        (
            user_id,
        )
    )


    row = cursor.fetchone()


    conn.close()


    return row




def update_profile(
    user_id,
    nickname=None,
    bio=None,
    interests=None
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users

        SET

        nickname=COALESCE(?,nickname),

        bio=COALESCE(?,bio),

        interests=COALESCE(?,interests)

        WHERE id=?

        """,
        (
            nickname,
            bio,
            interests,
            user_id,
        )
    )


    conn.commit()
    conn.close()

# ==========================
# Messages
# ==========================


def save_message(
    user_id,
    role,
    message
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO messages

        (
            user_id,
            role,
            message
        )

        VALUES(?,?,?)

        """,
        (
            user_id,
            role,
            message
        )
    )


    conn.commit()
    conn.close()




def get_history(
    user_id,
    limit=10
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        role,
        message

        FROM messages

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT ?

        """,
        (
            user_id,
            limit
        )
    )


    rows = cursor.fetchall()


    conn.close()


    return rows[::-1]




def clear_history(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM messages

        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    conn.commit()
    conn.close()





# ==========================
# Memory
# ==========================


def save_memory(
    user_id,
    key,
    value
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO memory

        (
            user_id,
            memory_key,
            memory_value
        )

        VALUES(?,?,?)

        ON CONFLICT(user_id,memory_key)

        DO UPDATE SET

        memory_value=excluded.memory_value

        """,
        (
            user_id,
            key,
            value
        )
    )


    conn.commit()
    conn.close()




def get_memories(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        memory_key,
        memory_value

        FROM memory

        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    result = cursor.fetchall()


    conn.close()


    return result




def clear_memory(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM memory

        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    conn.commit()
    conn.close()




def clear_user_memory(
    user_id
):

    clear_memory(
        user_id
    )





# ==========================
# State
# ==========================


def save_state(
    user_id,
    active_project=None,
    current_goal=None,
    preferences=None
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO user_state

        (
            user_id,
            active_project,
            current_goal,
            preferences
        )

        VALUES(?,?,?,?)

        ON CONFLICT(user_id)

        DO UPDATE SET

        active_project=excluded.active_project,

        current_goal=excluded.current_goal,

        preferences=excluded.preferences

        """,
        (
            user_id,
            active_project or "",
            current_goal or "",
            json.dumps(
                preferences or {},
                ensure_ascii=False
            )
        )
    )


    conn.commit()
    conn.close()




def get_state(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        active_project,

        current_goal,

        preferences

        FROM user_state

        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    row = cursor.fetchone()


    conn.close()



    if not row:

        return {

            "active_project": "",

            "current_goal": "",

            "preferences": {}

        }



    return {

        "active_project": row[0] or "",

        "current_goal": row[1] or "",

        "preferences":
            json.loads(row[2])
            if row[2]
            else {}

    }

# ==========================
# Broadcast
# ==========================

broadcast_messages = {}



def set_broadcast_message(
    user_id,
    value=True
):

    broadcast_messages[user_id] = value




def get_broadcast_message(
    user_id
):

    return broadcast_messages.get(
        user_id
    )




def clear_broadcast_message(
    user_id
):

    broadcast_messages.pop(
        user_id,
        None
    )


admin_actions = {}


def set_admin_action(
    user_id,
    action
):

    admin_actions[user_id] = action



def get_admin_action(
    user_id
):

    return admin_actions.get(
        user_id
    )



def clear_admin_action(
    user_id
):

    admin_actions.pop(
        user_id,
        None
    )



def get_total_messages():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM messages
        """
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count



def get_total_memories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM memory
        """
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count



def get_total_cached_questions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM qa_cache
        """
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count


# ==========================
# Plans
# ==========================

def get_user_plan(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT plan

        FROM users

        WHERE id=?

        """,
        (
            user_id,
        )
    )


    row = cursor.fetchone()


    conn.close()


    if row and row[0]:

        return row[0]


    return "free"




def update_user_plan(
    user_id,
    plan
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users

        SET plan=?

        WHERE id=?

        """,
        (
            plan,
            user_id
        )
    )


    conn.commit()
    conn.close()





# ==========================
# Usage
# ==========================


def add_usage(
    user_id,
    usage_type="messages"
):

    today = datetime.now().date().isoformat()


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR IGNORE INTO usage

        (
            user_id,
            date
        )

        VALUES(?,?)

        """,
        (
            user_id,
            today
        )
    )


    if usage_type not in [
        "messages",
        "images",
        "code_requests",
        "searches"
    ]:

        usage_type = "messages"



    cursor.execute(
        f"""
        UPDATE usage

        SET {usage_type}={usage_type}+1

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




def get_today_usage(
    user_id
):

    today = datetime.now().date().isoformat()


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
            today
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
# Subscriptions
# ==========================


def create_subscription(
    user_id,
    plan,
    days
):

    today = datetime.now().date().isoformat()


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO subscriptions

        (
            user_id,
            plan,
            start_date,
            duration_days,
            status
        )

        VALUES(?,?,?,?,?)

        ON CONFLICT(user_id)

        DO UPDATE SET

        plan=excluded.plan,

        start_date=excluded.start_date,

        duration_days=excluded.duration_days,

        status=excluded.status

        """,
        (
            user_id,
            plan,
            today,
            days,
            "active"
        )
    )


    conn.commit()
    conn.close()




def get_subscription(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        plan,

        start_date,

        duration_days,

        status

        FROM subscriptions

        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    row = cursor.fetchone()


    conn.close()


    if not row:

        return {

            "plan": "free",

            "start_date": "",

            "duration_days": 0,

            "status": "inactive"

        }



    return {

        "plan": row[0],

        "start_date": row[1],

        "duration_days": row[2],

        "status": row[3]

    }





# ==========================
# Rate Limit Database
# ==========================


def get_last_request(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT last_request

        FROM rate_limit

        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    row = cursor.fetchone()


    conn.close()


    return row[0] if row else 0




def update_last_request(
    user_id,
    timestamp
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO rate_limit

        (
            user_id,
            last_request
        )

        VALUES(?,?)

        ON CONFLICT(user_id)

        DO UPDATE SET

        last_request=excluded.last_request

        """,
        (
            user_id,
            timestamp
        )
    )


    conn.commit()
    conn.close()