import logging

from services.tasks.service import TaskService


logger = logging.getLogger(__name__)


class TaskPipeline:

    @staticmethod
    def execute(
        user_id: int,
        message: str,
        intent
    ):

        try:

            result = TaskService.create(
                user_id=user_id,
                message=message,
            )

            return {
                "response": (
                    "✅ یادآوری ثبت شد\n\n"
                    f"📝 {result.get('title', '')}\n"
                    f"🆔 {result.get('id', '')}"
                ),
                "cached": False,
                "intent": (
                    intent.to_dict()
                    if intent and hasattr(intent, "to_dict")
                    else {}
                ),
                "provider": "task",
            }

        except ValueError as e:

            logger.warning(
                "Task validation error: %s",
                e,
            )

            return {
                "response": f"⚠️ {str(e)}",
                "cached": False,
                "intent": (
                    intent.to_dict()
                    if intent and hasattr(intent, "to_dict")
                    else {}
                ),
                "provider": "task",
            }

        except Exception:

            logger.exception(
                "Task pipeline failed"
            )

            return {
                "response": "❌ خطا در ثبت یادآوری",
                "cached": False,
                "intent": (
                    intent.to_dict()
                    if intent and hasattr(intent, "to_dict")
                    else {}
                ),
                "provider": "task",
            }