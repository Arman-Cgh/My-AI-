import time

from database.plans import get_user_limits


# آخرین درخواست کاربران
user_last_message = {}


def check_rate_limit(user_id: int):

    limits = get_user_limits(user_id)

    cooldown = int(
        limits.get(
            "cooldown_seconds",
            5
        )
    )

    now = time.time()


    last_time = user_last_message.get(
        user_id
    )


    print("=" * 40)
    print("RATE LIMIT")
    print("USER:", user_id)
    print("LAST:", last_time)
    print("NOW:", now)
    print("COOLDOWN:", cooldown)


    # اولین پیام کاربر
    if last_time is None:

        user_last_message[user_id] = now

        print("FIRST MESSAGE")
        print("ALLOWED")

        return True



    diff = now - last_time


    print("DIFF:", diff)



    # بدون محدودیت
    if cooldown <= 0:

        user_last_message[user_id] = now

        print("NO LIMIT")

        return True



    # هنوز زمان نگذشته
    if diff < cooldown:

        remaining = cooldown - diff

        print(
            "BLOCKED",
            "WAIT:",
            round(remaining,2)
        )

        return False



    # اجازه پیام جدید
    user_last_message[user_id] = now

    print("ALLOWED")

    return True