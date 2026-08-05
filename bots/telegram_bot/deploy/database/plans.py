from database.db import get_connection
from database.subscriptions import get_subscription



# ==========================
# Get User Plan
# ==========================

def get_user_plan(user_id):

    subscription = get_subscription(user_id)

    if subscription.get("is_active"):
        return subscription["plan"]

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
        stored_plan = row[0]
        if (
            subscription["status"] in ["expired", "cancelled"]
            and subscription["plan"] == stored_plan
        ):
            return "free"

        return stored_plan


    return "free"



# ==========================
# Get Plan Settings
# ==========================

def get_plan_settings(plan_name):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
        
        daily_messages,
        daily_images,
        daily_technical_questions,
        cooldown_seconds
        
        FROM plans
        
        WHERE name=?
        
        """,
        (
            plan_name,
        )
    )


    row = cursor.fetchone()

    conn.close()


    if not row:

        return {

            "daily_messages": 30,

            "daily_images": 1,

            "daily_technical_questions": 3,

            "cooldown_seconds": 5

        }


    return {

        "daily_messages": row[0],

        "daily_images": row[1],

        "daily_technical_questions": row[2],

        "cooldown_seconds": row[3]

    }



# ==========================
# Get User Limits
# ==========================

def get_user_limits(user_id):

    plan = get_user_plan(
        user_id
    )


    return get_plan_settings(
        plan
    )