import asyncio

from services.ai.engine import AIEngine


async def main():

    ai = AIEngine()

    response = await ai.ask(
        user_id=1,
        user_message="پروژه AetherAI رو فردا بررسی کن",
        use_cache=False,
        extract_info=False,
    )

    print(
        "\n===== RESPONSE =====\n"
    )

    print(response)

    await ai.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

