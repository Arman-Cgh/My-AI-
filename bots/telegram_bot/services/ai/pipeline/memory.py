import asyncio
import logging

from services.ai.extractor import extract_memory
from services.ai.memory import MemoryService


logger = logging.getLogger(__name__)


class MemoryPipeline:

    KEYWORDS = (
        "یادم باشه",
        "یادت باشه",
        "ذخیره کن",
        "به خاطر بسپار",
        "فراموش نکن",
        "اسم من",
        "نام من",
        "یادم بمونه",
        "remember",
        "save",
        "my name",
    )

    SKIP_INTENTS = {
        "task",
        "code",
        "search",
        "image",
        "vision",
    }

    @classmethod
    def should_extract(
        cls,
        intent: str,
        message: str
    ) -> bool:

        if intent == "memory":
            return True

        if intent in cls.SKIP_INTENTS:
            return False

        text = (
            message or ""
        ).lower()

        return any(
            keyword.lower() in text
            for keyword in cls.KEYWORDS
        )

    @staticmethod
    async def extract(
        provider_manager,
        provider_name: str,
        user_id: int,
        message: str,
        response: str
    ):

        try:

            result = await extract_memory(
                provider=provider_manager,
                provider_name=provider_name,
                user_id=user_id,
                user_message=message,
                assistant_response=response
            )

            if not result:
                return

            MemoryService.apply(
                user_id=user_id,
                memory=result.get(
                    "memory",
                    {}
                ),
                state=result.get(
                    "state",
                    {}
                )
            )

        except Exception:

            logger.exception(
                "Memory extraction failed"
            )

    @classmethod
    def schedule(
        cls,
        provider_manager,
        provider_name,
        user_id,
        message,
        response
    ):

        asyncio.create_task(
            cls.extract(
                provider_manager=provider_manager,
                provider_name=provider_name,
                user_id=user_id,
                message=message,
                response=response
            )
        )