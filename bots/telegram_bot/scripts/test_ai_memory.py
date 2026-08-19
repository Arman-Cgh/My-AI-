import asyncio

from database.db import init_db
from services.ai.engine import AIEngine
from services.ai.context import ContextBuilder


init_db()


async def test():

    user_id = 1

    message = (
        "اسم من یونس است. "
        "من برنامه نویس پایتون هستم "
        "و به هوش مصنوعی علاقه دارم."
    )


    engine = AIEngine()


    result = await engine.generate_response(
        user_id=user_id,
        message=message,
        use_cache=False
    )
    await asyncio.sleep(3)


    print(
        "\n===== AI RESULT =====\n"
    )

    print(result)


    print(
        "\n===== CONTEXT AFTER MEMORY =====\n"
    )


    context = ContextBuilder(
        user_id
    ).build()


    print(context)



if __name__ == "__main__":

    asyncio.run(test())