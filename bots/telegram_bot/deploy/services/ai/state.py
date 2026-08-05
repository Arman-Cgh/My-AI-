from database.db import get_state


class UserState:

    def __init__(self, user_id:int):
        self.user_id = user_id


    def get(self):

        return get_state(
            self.user_id
        )