import asyncio

from services.ai.engine import AIEngine


async def main():

    engine = AIEngine()

    await engine.initialize()

    print("ENGINE READY")

    result = await engine.generate_response(
        user_id=123456,
        message="سلام، خودتو معرفی کن",
        use_cache=False,
        extract_info=False
    )

    print("\nRESULT:")
    print(result)

    await engine.shutdown()


if __name__ == "__main__":
    asyncio.run(main())