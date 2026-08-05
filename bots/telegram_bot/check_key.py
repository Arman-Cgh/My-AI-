from openai import OpenAI

from services.ai.config import (
    AI_API_KEY,
    AI_BASE_URL,
    AI_MODEL
)


print("BASE:", AI_BASE_URL)
print("MODEL:", AI_MODEL)
print("KEY:", AI_API_KEY[:12])


client = OpenAI(
    api_key=AI_API_KEY,
    base_url=AI_BASE_URL
)


response = client.chat.completions.create(

    model=AI_MODEL,

    messages=[
        {
            "role": "user",
            "content": "سلام، خودتو معرفی کن"
        }
    ]

)


print(
    response.choices[0].message.content
)