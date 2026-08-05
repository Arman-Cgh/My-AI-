import asyncio

from services.ai.extractor import extract_memory
from database.db import get_memories, init_db


USER_ID = 888888


async def main():

    init_db()

    result = await extract_memory(
        USER_ID,
        "من دارم روی پروژه AetherAI کار می‌کنم. هدفم ساخت یک دستیار هوشمند شخصی است.",
        "خیلی خوب، AetherAI پروژه جالبی است."
    )

    print("\nEXTRACT RESULT:")
    print(result)


    print("\nDATABASE MEMORY:")

    memories = get_memories(USER_ID)

    for item in memories:
        print(item)


asyncio.run(main())