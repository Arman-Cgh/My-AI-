from datetime import datetime

from database.db import (
    get_profile,
    get_memories,
    get_history,
)

from services.ai.state import UserState


class ContextBuilder:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def build(self):

        # ==========================
        # Profile
        # ==========================

        profile_data = get_profile(self.user_id)

        if profile_data:

            profile = {
                "username": profile_data[0] or "",
                "first_name": profile_data[1] or "",
                "nickname": profile_data[2] or "",
                "bio": profile_data[3] or "",
                "interests": profile_data[4] or "",
            }

        else:

            profile = {
                "username": "",
                "first_name": "",
                "nickname": "",
                "bio": "",
                "interests": "",
            }

        # ==========================
        # Long Memory
        # ==========================

        memories = get_memories(self.user_id)

        if memories:

            memory_lines = []

            for key, value in sorted(memories):
                memory_lines.append(f"- {key}: {value}")

            memory_text = (
                "حافظه بلند مدت کاربر:\n"
                + "\n".join(memory_lines)
            )

        else:

            memory_text = "حافظه‌ای ثبت نشده است."

        # ==========================
        # Short History
        # ==========================

        history_rows = get_history(
            self.user_id,
            limit=6
        )

        history = []

        for role, message in history_rows:

            history.append(
                {
                    "role": role,
                    "content": message
                }
            )

        # ==========================
        # User State
        # ==========================

        state = UserState(
            self.user_id
        ).get()

        # ==========================
        # Final Context
        # ==========================

        return {

            "profile": profile,

            "memory": memory_text,

            "history": history,

            "state": state,

            "datetime": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

        }