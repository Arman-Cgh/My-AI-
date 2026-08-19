from services.conversation.session import ConversationSession

from database.db import (
    save_message,
    get_history
)


class ConversationManager:


    def __init__(
        self,
        max_messages=20
    ):

        self.session = ConversationSession()

        self.max_messages = max_messages



    # ==========================
    # Add User Message
    # ==========================

    def add_user_message(
        self,
        user_id,
        message
    ):

        self._ensure_loaded(
            user_id
        )


        self.session.add_message(
            user_id,
            "user",
            message
        )


        save_message(
            user_id,
            "user",
            message
        )


        self._trim(
            user_id
        )



    # ==========================
    # Add Assistant Message
    # ==========================

    def add_assistant_message(
        self,
        user_id,
        message
    ):

        self._ensure_loaded(
            user_id
        )


        self.session.add_message(
            user_id,
            "assistant",
            message
        )


        save_message(
            user_id,
            "assistant",
            message
        )


        self._trim(
            user_id
        )



    # ==========================
    # Get History
    # ==========================

    def get_history(
        self,
        user_id
    ):


        messages = self.session.get_messages(
            user_id
        )


        if messages:

            return messages



        history = get_history(
            user_id,
            self.max_messages
        )


        for role, message in history:

            self.session.add_message(
                user_id,
                role,
                message
            )


        return self.session.get_messages(
            user_id
        )



    # ==========================
    # Clear Conversation
    # ==========================

    def clear(
        self,
        user_id
    ):

        self.session.clear_messages(
            user_id
        )



    # ==========================
    # Metadata
    # ==========================

    def set_metadata(
        self,
        user_id,
        key,
        value
    ):

        self.session.set_metadata(
            user_id,
            key,
            value
        )



    def get_metadata(
        self,
        user_id,
        key,
        default=None
    ):

        return self.session.get_metadata(
            user_id,
            key,
            default
        )



    # ==========================
    # Load From Database
    # ==========================

    def _ensure_loaded(
        self,
        user_id
    ):

        if self.session.get(
            user_id
        ):

            return



        history = get_history(
            user_id,
            self.max_messages
        )


        for role, message in history:

            self.session.add_message(
                user_id,
                role,
                message
            )



    # ==========================
    # Trim
    # ==========================

    def _trim(
        self,
        user_id
    ):

        messages = self.session.get_messages(
            user_id,
            limit=999
        )


        if len(messages) <= self.max_messages:

            return



        excess = (
            len(messages)
            -
            self.max_messages
        )


        self.session.remove_oldest(
            user_id,
            excess
        )