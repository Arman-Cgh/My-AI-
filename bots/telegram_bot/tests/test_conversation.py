import asyncio

from database.db import (
    init_db,
    add_user,
)

from services.conversation.handler import ConversationHandler


TEST_USER_ID = 1


async def main():

    init_db()

    add_user(
        user_id=TEST_USER_ID,
        username="conversation_test",
        first_name="Test",
    )

    handler = ConversationHandler()

    # ==========================================
    # 1. Chat
    # ==========================================

    print("\n===== CHAT =====\n")

    chat_response = await handler.handle(
        user_id=TEST_USER_ID,
        message="سلام، حالت چطوره؟",
    )

    print(chat_response)

    # ==========================================
    # 2. Task
    # ==========================================

    print("\n===== TASK =====\n")

    task_response = await handler.handle(
        user_id=TEST_USER_ID,
        message="پروژه AetherAI رو فردا بررسی کن",
    )

    print(task_response)

    # ==========================================
    # 3. Empty Message
    # ==========================================

    print("\n===== EMPTY MESSAGE =====\n")

    empty_response = await handler.handle(
        user_id=TEST_USER_ID,
        message="",
    )

    print(empty_response)

    # ==========================================
    # 4. History
    # ==========================================

    print("\n===== HISTORY =====\n")

    history = handler.conversation.history(
        TEST_USER_ID,
    )

    for message in history:
        print(message)

    # ==========================================
    # 5. Shutdown
    # ==========================================

    await handler.ai.shutdown()

    print("\n===== TEST COMPLETED =====\n")


if __name__ == "__main__":
    asyncio.run(main())