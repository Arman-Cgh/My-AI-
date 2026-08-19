from database.db import init_db, add_user
from services.conversation.service import ConversationService


def test_task_message_routing():

    init_db()

    user_id = 666666

    add_user(
        user_id=user_id,
        username="conversation_test",
        first_name="Conversation Test",
    )

    service = ConversationService()

    result = service.process(
        user_id=user_id,
        message="فردا ساعت ۱۰ یادم بنداز قبض را پرداخت کنم",
    )

    assert result["allowed"] is True

    route = result["route"]

    assert route is not None

    assert (
        route.get("action")
        == "task"
    )