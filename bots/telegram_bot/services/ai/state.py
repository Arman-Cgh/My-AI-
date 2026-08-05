from database.db import get_state



class UserState:


    def __init__(
        self,
        user_id:int
    ):

        self.user_id = user_id



    def get(self):

        state = get_state(
            self.user_id
        )


        if not state:

            return {

                "active_project": "",

                "current_goal": "",

                "last_topic": "",

                "working_on": "",

                "preferences": {}

            }


        return state