from openai import OpenAI

from config import TOKENFAUCET_API_KEY


client = OpenAI(
    api_key=TOKENFAUCET_API_KEY,
    base_url="https://freetokenfaucet.com/v1"
)


async def get_tokenfaucet_response(message: str, context=""):

    try:

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": f"""
Conversation history:
{context}

User message:
{message}
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("TokenFaucet Error:", e)
        return "خطا در اتصال به AI"