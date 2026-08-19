from database.db import (
    get_memories,
    save_memory,
    get_state,
    save_state,
)

from services.ai.profile_manager import ProfileManager


class MemoryService:

    ALLOWED_MEMORY_KEYS = {
        "name",
        "job",
        "interests",
        "location",
        "preferences",
    }

    MEMORY_KEY_ALIASES = {
        "nickname": "name",
        "full_name": "name",
        "username": "name",

        "profession": "job",
        "occupation": "job",
        "work": "job",
        "career": "job",
        "field": "job",

        "hobby": "interests",
        "interest": "interests",
    }

    MAX_VALUE_LENGTH = 100

    # ==========================
    # Memory
    # ==========================

    @classmethod
    def get_memory(
        cls,
        user_id: int
    ):

        rows = get_memories(
            user_id
        )

        return {
            key: value
            for key, value in (rows or [])
        }

    @classmethod
    def normalize_memory_key(
        cls,
        key
    ):

        key = str(
            key
        ).strip().lower()

        return cls.MEMORY_KEY_ALIASES.get(
            key,
            key
        )

    @classmethod
    def normalize_memory_value(
        cls,
        value
    ):

        if value is None:
            return ""

        if isinstance(
            value,
            list
        ):

            value = ", ".join(
                map(
                    str,
                    value
                )
            )

        value = str(
            value
        ).strip()

        if not value:
            return ""

        if len(value) > cls.MAX_VALUE_LENGTH:
            return ""

        return value

    @classmethod
    def update_memory(
        cls,
        user_id: int,
        memory: dict
    ):

        if not isinstance(
            memory,
            dict
        ):

            return {}

        current = cls.get_memory(
            user_id
        )

        updated = {}

        for key, value in memory.items():

            key = cls.normalize_memory_key(
                key
            )

            if key not in cls.ALLOWED_MEMORY_KEYS:
                continue

            value = cls.normalize_memory_value(
                value
            )

            if not value:
                continue

            if current.get(key) == value:
                continue

            save_memory(
                user_id,
                key,
                value
            )

            updated[key] = value

        if updated:

            ProfileManager.update(
                user_id,
                updated
            )

        return updated

    # ==========================
    # State
    # ==========================

    @classmethod
    def get_state(
        cls,
        user_id: int
    ):

        return get_state(
            user_id
        ) or {}

    @classmethod
    def update_state(
        cls,
        user_id: int,
        state: dict
    ):

        if not isinstance(
            state,
            dict
        ):

            return {}

        current = cls.get_state(
            user_id
        )

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

        return {
            "active_project": active_project,
            "current_goal": current_goal,
            "preferences": preferences,
        }

    # ==========================
    # Combined update
    # ==========================

    @classmethod
    def apply(
        cls,
        user_id: int,
        memory: dict | None = None,
        state: dict | None = None
    ):

        updated_memory = cls.update_memory(
            user_id,
            memory or {}
        )

        updated_state = cls.update_state(
            user_id,
            state or {}
        ) if state else {}

        return {
            "memory": updated_memory,
            "state": updated_state,
        }