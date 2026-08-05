import asyncio

from services.ai.providers.manager import ProviderManager


async def main():

    provider = ProviderManager().get_provider()

    response = await provider.generate(
        [
            {
                "role": "user",
                "content": "سلام، خودتو معرفی کن"
            }
        ]
    )

    print("\n===== RESPONSE =====")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())