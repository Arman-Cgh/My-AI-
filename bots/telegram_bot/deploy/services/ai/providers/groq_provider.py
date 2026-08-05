from openai import AsyncOpenAI

from .base import AIProvider

from services.ai.config import (
    AI_API_KEY,
    AI_BASE_URL,
    AI_MODEL,
    MAX_TOKENS,
    TEMPERATURE
)


class GroqProvider(AIProvider):

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL
        )

    async def generate(
        self,
        messages: list,
        model: str = None
    ):

        response = await self.client.chat.completions.create(
            model=model or AI_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )

        return response.choices[0].message.content