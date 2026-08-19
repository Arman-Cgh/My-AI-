import logging

from services.conversation.service import ConversationService
from services.ai.engine import AIEngine
from services.ai.pipeline.task import TaskPipeline


logger = logging.getLogger(__name__)


class ConversationHandler:

    def __init__(
        self,
        conversation=None,
        ai=None,
    ):

        self.conversation = (
            conversation
            or ConversationService()
        )

        self.ai = (
            ai
            or AIEngine()
        )

    async def handle(
        self,
        user_id: int,
        message: str,
    ):

        result = self.conversation.process(
            user_id=user_id,
            message=message,
        )

        if not result["allowed"]:

            return result.get(
                "reason",
                "درخواست رد شد.",
            )

        clean_message = result["message"]
        route = result["route"]
        intent = result["intent"]

        # ==========================================
        # Non-AI Routes
        # ==========================================

        if not route.get(
            "requires_ai",
            True,
        ):

            return await self._handle_non_ai_route(
                user_id=user_id,
                message=clean_message,
                route=route,
                intent=intent,
            )

        # ==========================================
        # AI Pipeline
        # ==========================================

        try:

            ai_result = await self.ai.generate_response(
                user_id=user_id,
                message=clean_message,
                intent=intent,
            )

        except Exception:

            logger.exception(
                "AI pipeline failed",
            )

            raise

        response = ai_result.get(
            "response",
            "",
        )

        response = (
            self.conversation.middleware.after_process(
                response,
            )
        )

        # ==========================================
        # Save Assistant Response
        # ==========================================

        if route.get(
            "save_history",
            True,
        ):

            self.conversation.save_response(
                user_id=user_id,
                response=response,
            )

        return response

    # ==========================================
    # Non-AI Routes
    # ==========================================

    async def _handle_non_ai_route(
        self,
        user_id: int,
        message: str,
        route: dict,
        intent,
    ):

        action = route.get(
            "action",
            "chat",
        )

        # ==========================================
        # Task
        # ==========================================

        if action == "task":

            try:

                result = TaskPipeline.execute(
                    user_id=user_id,
                    message=message,
                    intent=intent,
                )

                response = result.get(
                    "response",
                    "",
                )

                response = (
                    self.conversation.middleware.after_process(
                        response,
                    )
                )

                if route.get(
                    "save_history",
                    True,
                ):

                    self.conversation.save_response(
                        user_id=user_id,
                        response=response,
                    )

                return response

            except Exception:

                logger.exception(
                    "Task pipeline failed",
                )

                raise

        # ==========================================
        # Future Non-AI Routes
        # ==========================================

        return (
            "این قابلیت هنوز پیاده‌سازی نشده است."
        )