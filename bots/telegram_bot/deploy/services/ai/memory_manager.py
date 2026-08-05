from database.db import (
    save_memory,
    get_memories
)


class MemoryManager:

    @staticmethod
    def update(user_id: int, memory: dict):

        if not memory:
            return

        current = dict(get_memories(user_id))

        for key, value in memory.items():

            if value is None:
                continue

            if isinstance(value, list):
                value = ", ".join(value)

            value = str(value).strip()

            if not value:
                continue

            old = current.get(key)

            # اگر تغییر نکرده
            if old == value:
                continue

            # ذخیره یا بروزرسانی
            save_memory(
                user_id,
                key,
                value
            )