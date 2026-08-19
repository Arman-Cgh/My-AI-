import pytest

from database.db import (
    init_db,
    add_user,
)

from services.conversation.handler import ConversationHandler


class FakeAI:

    async def generate_response(
        self,
        user_id,
        message,
        intent=None,
    ):

        return {
            "response": "پاسخ تستی AI",
            "cached": False,
            "provider": "fake",
        }



@pytest.fixture
def test_user():

    init_db()

    user_id = 123456

    add_user(
        user_id=user_id,
        username="flow_test",
        first_name="Flow",
    )

    return user_id



@pytest.mark.asyncio
async def test_normal_chat_flow(test_user):

    handler = ConversationHandler(
        ai=FakeAI()
    )

    result = await handler.handle(
        user_id=test_user,
        message="سلام",
    )

    assert result == "پاسخ تستی AI"



@pytest.mark.asyncio
async def test_task_routing_flow(test_user):

    handler = ConversationHandler(
        ai=FakeAI()
    )

    result = await handler.handle(
        user_id=test_user,
        message="فردا ساعت 10 یادم بنداز تست انجام شود",
    )

    assert result is not None