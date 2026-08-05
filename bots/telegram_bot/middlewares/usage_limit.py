from database.plans import get_user_limits
from database.usage import can_send_message



def check_usage_limit(
    user_id
):

    limits = get_user_limits(
        user_id
    )


    daily_limit = limits[
        "daily_messages"
    ]


    return can_send_message(
        user_id,
        daily_limit
    )