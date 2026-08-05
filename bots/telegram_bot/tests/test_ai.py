import asyncio

from database.db import init_db
from services.ai.engine import AIEngine
from services.ai.context import ContextBuilder


# ساخت جدول‌ها
init_db()



async def test():

    user_id = 1


    message = (
        "اسم من یونس است. "
        "من برنامه نویس پایتون هستم "
        "و به هوش مصنوعی علاقه دارم."
    )


    engine = AIEngine()

    response = await engine.ask(
        user_id,
        message
)


    print("\n===== CONTEXT AFTER MEMORY =====\n")


    context = ContextBuilder(
        user_id
    ).build()


    print(context)



    print("\n===== AI RESPONSE =====\n")


    print(response)



if __name__ == "__main__":
    asyncio.run(test())