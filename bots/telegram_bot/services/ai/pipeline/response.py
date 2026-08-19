from typing import Dict, Any

from services.ai.context import ContextBuilder
from services.ai.prompt import build_prompt


class ResponsePipeline:

    def __init__(
        self,
        provider_manager,
        cache
    ):

        self.provider_manager = provider_manager
        self.cache = cache

    async def build_messages(
        self,
        user_id: int,
        message: str,
        intent: str
    ):

        context = ContextBuilder(
            user_id
        ).build(
            intent=intent
        )

        return build_prompt(
            user_id=user_id,
            user_message=message,
            context=context
        )

    async def generate(
        self,
        user_id: int,
        message: str,
        intent: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:

        if use_cache:

            cached = await self.cache.get(
                user_id,
                message
            )

            if cached:

                return {
                    "response": cached,
                    "cached": True,
                    "intent": {
                        "intent": "cached",
                        "confidence": 1,
                        "source": "cache"
                    },
                    "provider": "cache"
                }

        messages = await self.build_messages(
            user_id=user_id,
            message=message,
            intent=intent
        )

        result = await self.provider_manager.generate(
            messages
        )

        response = result.get(
            "text",
            ""
        )

        provider = result.get(
            "provider",
            "unknown"
        )

        if use_cache:

            await self.cache.set(
                user_id,
                message,
                response
            )

        return {
            "response": response,
            "cached": False,
            "provider": provider
        }