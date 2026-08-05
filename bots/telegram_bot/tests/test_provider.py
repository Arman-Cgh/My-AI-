import asyncio

from services.ai.providers.manager import ProviderManager


async def main():

    manager = ProviderManager()

    provider = manager.get_provider()

    response = await provider.generate(
        [
            {
                "role": "user",
                "content": "سلام، خودت را معرفی کن"
            }
        ],
        "llama-3.3-70b-versatile"
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())