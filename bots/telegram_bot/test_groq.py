import asyncio
from openai import AsyncOpenAI

from services.ai.config import AI_API_KEY, AI_BASE_URL


async def main():

    client = AsyncOpenAI(
        api_key=AI_API_KEY,
        base_url=AI_BASE_URL
    )

    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "سلام، خودتو معرفی کن"
            }
        ]
    )

    print(response.choices[0].message.content)


asyncio.run(main())
