from database.db import (
    save_message,
    get_history
)


class ConversationManager:


    MAX_CONTEXT_MESSAGES = 20



    @staticmethod
    def add_message(
        user_id:int,
        role:str,
        content:str
    ):

        if not content:
            return


        save_message(
            user_id,
            role,
            content
        )



    @staticmethod
    def get_history(
        user_id:int,
        limit=None
    ):

        limit = (
            limit
            or
            ConversationManager.MAX_CONTEXT_MESSAGES
        )


        rows = get_history(
            user_id,
            limit
        )


        return [
            {
                "role": role,
                "content": message
            }

            for role,message in rows
            if message
        ]



    @staticmethod
    def needs_summary(
        user_id:int
    ):

        history = ConversationManager.get_history(
            user_id,
            100
        )


        return len(history) > ConversationManager.MAX_CONTEXT_MESSAGES