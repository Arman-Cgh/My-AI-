from datetime import datetime, timedelta


class ConversationSession:


    SESSION_TIMEOUT_MINUTES = 30



    def __init__(self):

        self.sessions = {}



    # ==========================
    # Create / Get Session
    # ==========================

    def get_or_create(
        self,
        user_id: int
    ):


        if user_id not in self.sessions:


            self.sessions[user_id] = {

                "user_id": user_id,

                "messages": [],

                "metadata": {},

                "created_at": datetime.now(),

                "updated_at": datetime.now()

            }



        self.sessions[user_id]["updated_at"] = datetime.now()


        return self.sessions[user_id]



    def get(
        self,
        user_id: int
    ):


        session = self.sessions.get(
            user_id
        )


        if not session:

            return None



        if self.is_expired(
            user_id
        ):

            self.delete(
                user_id
            )

            return None



        return session



    # ==========================
    # Messages
    # ==========================

    def add_message(
        self,
        user_id: int,
        role: str,
        content: str
    ):


        session = self.get_or_create(
            user_id
        )


        session["messages"].append({

            "role": role,

            "content": content,

            "time": datetime.now().isoformat()

        })


        session["updated_at"] = datetime.now()



    def get_messages(
        self,
        user_id: int,
        limit: int = 10
    ):


        session = self.get(
            user_id
        )


        if not session:

            return []



        return session["messages"][-limit:]



    def clear_messages(
        self,
        user_id: int
    ):


        session = self.get(
            user_id
        )


        if session:

            session["messages"] = []



    def remove_oldest(
        self,
        user_id: int,
        count: int
    ):


        session = self.get(
            user_id
        )


        if not session:

            return



        if count <= 0:

            return



        session["messages"] = session["messages"][count:]



    # ==========================
    # Metadata
    # ==========================

    def set_metadata(
        self,
        user_id: int,
        key: str,
        value
    ):


        session = self.get_or_create(
            user_id
        )


        session["metadata"][key] = value

        session["updated_at"] = datetime.now()



    def get_metadata(
        self,
        user_id: int,
        key: str,
        default=None
    ):


        session = self.get(
            user_id
        )


        if not session:

            return default



        return session["metadata"].get(
            key,
            default
        )



    def get_all_metadata(
        self,
        user_id: int
    ):


        session = self.get(
            user_id
        )


        if not session:

            return {}



        return session["metadata"]



    # ==========================
    # Lifecycle
    # ==========================

    def is_expired(
        self,
        user_id: int
    ):


        session = self.sessions.get(
            user_id
        )


        if not session:

            return True



        expire_time = (

            session["updated_at"]

            +

            timedelta(
                minutes=self.SESSION_TIMEOUT_MINUTES
            )

        )


        return datetime.now() > expire_time



    def delete(
        self,
        user_id: int
    ):

        self.sessions.pop(
            user_id,
            None
        )



    def clear_all(
        self
    ):

        self.sessions.clear()