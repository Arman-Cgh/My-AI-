import asyncio

from services.ai.engine import AIEngine


async def main():

    ai = AIEngine()

    response = await ai.ask(
        user_id=1,
        user_message="سلام، خودتو معرفی کن"
    )

    print("\n===== RESPONSE =====\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())