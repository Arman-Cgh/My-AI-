import datetime

from services.ai.memory import MemoryService
from services.ai.profile_manager import ProfileManager
from services.ai.context_optimizer import ContextOptimizer

from database.db import get_history


class ContextBuilder:

    def __init__(
        self,
        user_id: int
    ):
        self.user_id = user_id

    # ==========================
    # Memory
    # ==========================

    def _build_memory(self):

        try:

            memory = MemoryService.get_memory(
                self.user_id
            )

        except Exception:

            memory = {}

        if not memory:

            return (
                "╪¡╪º┘ü╪╕┘çΓÇî╪º█î ╪½╪¿╪¬ "
                "┘å╪┤╪»┘ç ╪º╪│╪¬."
            )

        return memory

    # ==========================
    # History
    # ==========================

    def _build_history(self):

        try:

            history = get_history(
                self.user_id,
                limit=10
            )

        except Exception:

            history = []

        normalized = []

        for item in history:

            # Database format:
            # (role, message)

            if isinstance(item, tuple):

                if len(item) < 2:
                    continue

                role = item[0]
                content = item[1]

            # Already normalized format

            elif isinstance(item, dict):

                role = item.get(
                    "role",
                    ""
                )

                content = item.get(
                    "content",
                    item.get(
                        "message",
                        ""
                    )
                )

            else:

                continue

            if not content:
                continue

            normalized.append(
                {
                    "role": str(role),
                    "content": str(content),
                }
            )

        return normalized

    # ==========================
    # Build
    # ==========================

    def build(
        self,
        intent="chat"
    ):

        context = {}

        # ==========================
        # Profile
        # ==========================

        try:

            profile = ProfileManager.get(
                self.user_id
            )

        except Exception:

            profile = {}

        context["profile"] = profile or {}

        # ==========================
        # Memory
        # ==========================

        context["memory"] = (
            self._build_memory()
        )

        # ==========================
        # History
        # ==========================

        if intent not in (
            "code",
            "memory"
        ):

            context["history"] = (
                self._build_history()
            )

        else:

            context["history"] = []

        # ==========================
        # State
        # ==========================

        try:

            state = MemoryService.get_state(
                self.user_id
            )

        except Exception:

            state = {}

        context["state"] = state or {}

        # ==========================
        # Optimize
        # ==========================

        try:

            context = ContextOptimizer.optimize(
                context,
                intent
            )

        except Exception:

            pass

        # ==========================
        # Time
        # ==========================

        context["datetime"] = (
            datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )

        return context

