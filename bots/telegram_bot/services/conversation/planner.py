from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationPlan:

    action: str

    intent: str

    requires_ai: bool = True

    save_history: bool = True


class ConversationPlanner:

    ROUTES = {
        "task": {
            "action": "task",
            "requires_ai": False,
        },
        "memory": {
            "action": "memory",
            "requires_ai": False,
        },
        "code": {
            "action": "code",
            "requires_ai": True,
        },
        "image": {
            "action": "image",
            "requires_ai": False,
        },
        "vision": {
            "action": "vision",
            "requires_ai": True,
        },
        "search": {
            "action": "search",
            "requires_ai": True,
        },
        "chat": {
            "action": "chat",
            "requires_ai": True,
        },
    }

    def create_plan(
        self,
        intent,
    ):

        intent_name = self._normalize_intent(
            intent
        )

        route = self.ROUTES.get(
            intent_name,
            self.ROUTES["chat"],
        )

        return ConversationPlan(
            action=route["action"],
            intent=intent_name,
            requires_ai=route["requires_ai"],
            save_history=True,
        )

    @staticmethod
    def _normalize_intent(
        intent,
    ):

        if hasattr(intent, "intent"):

            intent = intent.intent

        elif isinstance(intent, dict):

            intent = intent.get(
                "intent",
                "chat",
            )

        if not intent:

            return "chat"

        return str(
            intent
        ).strip().lower()