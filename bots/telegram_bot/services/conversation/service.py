from services.conversation.middleware import ConversationMiddleware
from services.conversation.router import ConversationRouter
from services.conversation.manager import ConversationManager

from services.ai.intent_router import IntentRouter


class ConversationService:

    def __init__(
        self,
        middleware=None,
        router=None,
        manager=None,
    ):

        self.middleware = (
            middleware
            or ConversationMiddleware()
        )

        self.router = (
            router
            or ConversationRouter()
        )

        self.manager = (
            manager
            or ConversationManager()
        )

    # ==========================================
    # Process Message
    # ==========================================

    def process(
        self,
        user_id: int,
        message: str,
        intent=None,
    ):

        checked = self.middleware.before_process(
            user_id,
            message,
        )

        if not checked["allowed"]:

            return {
                "allowed": False,
                "reason": checked.get(
                    "message",
                    "blocked",
                ),
            }

        clean_message = checked["message"]

        # ==========================================
        # Intent Detection
        # ==========================================

        if intent is None:

            intent = IntentRouter.detect(
                clean_message,
            )

        # ==========================================
        # Save User Message
        # ==========================================

        self.manager.add_user_message(
            user_id,
            clean_message,
        )

        # ==========================================
        # Routing
        # ==========================================

        route = self.router.route(
            intent,
        )

        return {
            "allowed": True,
            "user_id": user_id,
            "message": clean_message,
            "route": route,
            "intent": intent,
        }

    # ==========================================
    # Save Response
    # ==========================================

    def save_response(
        self,
        user_id: int,
        response: str,
    ):

        self.manager.add_assistant_message(
            user_id,
            response,
        )

    # ==========================================
    # History
    # ==========================================

    def history(
        self,
        user_id: int,
    ):

        return self.manager.get_history(
            user_id,
        )

    # ==========================================
    # Clear
    # ==========================================

    def clear(
        self,
        user_id: int,
    ):

        self.manager.clear(
            user_id,
        )