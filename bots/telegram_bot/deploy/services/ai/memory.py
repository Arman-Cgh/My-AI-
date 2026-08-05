from database.db import get_memories, save_memory, get_history
class MemoryEngine:

    def __init__(self, user_id: int):
        self.user_id = user_id


    def get_short_memory(self, limit: int = 20):

        history = get_history(
            self.user_id,
            limit=limit
        )

        if not history:
            return "تاریخچه‌ای وجود ندارد."

        text = ""

        for role, message in history:
            text += f"""
[{role}]
{message}

"""

        return text.strip()



    def get_long_memory(self):

        memories = get_memories(
            self.user_id
        )

        if not memories:
            return "حافظه‌ای ثبت نشده است."

        text = ""

        for key, value in memories:
            text += f"""
{key}: {value}
"""

        return text.strip()



    def build(self):

        return {
            "short_memory": self.get_short_memory(),
            "long_memory": self.get_long_memory()
        }