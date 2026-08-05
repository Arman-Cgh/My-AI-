from datetime import datetime

from database.db import (
    get_profile,
    get_memories,
    get_history,
)

from services.ai.state import UserState
from services.ai.context_optimizer import ContextOptimizer


class ContextBuilder:


    def __init__(
        self,
        user_id: int
    ):

        self.user_id = user_id



    def _default_profile(self):

        return {

            "username": "",
            "first_name": "",
            "nickname": "",
            "bio": "",
            "interests": "",

        }



    def _build_profile(self):

        profile = self._default_profile()


        data = get_profile(
            self.user_id
        )


        if data:

            profile.update({

                "username": data[0] or "",

                "first_name": data[1] or "",

                "nickname": data[2] or "",

                "bio": data[3] or "",

                "interests": data[4] or "",

            })


        return profile




    def _build_memory(self):

        memories = get_memories(
            self.user_id
        )


        if not memories:

            return "حافظه‌ای ثبت نشده است."


        lines = []


        for key, value in sorted(memories)[:30]:

            if value:

                lines.append(
                    f"- {key}: {value}"
                )


        if not lines:

            return "حافظه‌ای ثبت نشده است."


        return (
            "حافظه بلند مدت کاربر:\n"
            +
            "\n".join(lines)
        )




    def _clean_history(self, rows):

        result = []

        seen = set()


        for role, message in rows:

            if not message:

                continue


            key = (
                role,
                message.strip()
            )


            if key in seen:

                continue


            seen.add(key)


            result.append({

                "role": role,

                "content": message.strip()

            })


        return result




    def _build_history(self):

        rows = get_history(
            self.user_id,
            limit=20
        )


        history = self._clean_history(
            rows
        )


        return history[-8:]




    def build(
        self,
        intent="chat"
    ):


        # برای کدنویسی context شخصی ارسال نشود

        if intent == "code":

            return {

                "profile": {},

                "memory": "",

                "history": [],

                "state": {},

                "datetime": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )

            }



        profile = self._build_profile()


        memory = self._build_memory()


        history = self._build_history()


        state = UserState(
            self.user_id
        ).get()



        optimized = ContextOptimizer.optimize(

            profile,

            memory,

            history,

            state

        )



        return {

            **optimized,

            "datetime": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )

        }