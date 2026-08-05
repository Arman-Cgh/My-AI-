from database.db import get_all_users


def get_users_count():

    return len(get_all_users())