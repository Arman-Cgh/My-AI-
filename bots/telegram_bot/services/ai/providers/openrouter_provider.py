from openai import AsyncOpenAI

from services.ai.config import (
    AI_API_KEY,
    AI_BASE_URL,
    MAX_TOKENS,
    TEMPERATURE
)


class OpenRouterProvider:


    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL
        )



    async def generate(
        self,
        messages,
        model
    ):

        response = await self.client.chat.completions.create(

            model=model,

            messages=messages,

            max_tokens=MAX_TOKENS,

            temperature=TEMPERATURE

        )


        return response.choices[0].message.content