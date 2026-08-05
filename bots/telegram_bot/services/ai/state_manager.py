from database.db import (
    get_state,
    save_state
)



class StateManager:



    @staticmethod
    def update(
        user_id:int,
        state:dict
    ):


        if not state:

            return



        current = get_state(
            user_id
        ) or {}



        active_project = state.get(
            "active_project",
            current.get(
                "active_project",
                ""
            )
        )



        current_goal = state.get(
            "current_goal",
            current.get(
                "current_goal",
                ""
            )
        )



        preferences = state.get(
            "preferences",
            current.get(
                "preferences",
                {}
            )
        )



        save_state(

            user_id,

            active_project,

            current_goal,

            preferences

        )