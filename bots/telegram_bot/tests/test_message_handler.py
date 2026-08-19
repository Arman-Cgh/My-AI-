import pytest

from handlers.message import handle_message


class FakeMessage:

    def __init__(self):
        self.responses = []

        self.text = "سلام"

    async def reply_text(
        self,
        text,
    ):
        self.responses.append(text)



class FakeUser:

    id = 777777
    username = "handler_test"
    first_name = "Handler"



class FakeUpdate:

    def __init__(self):

        self.message = FakeMessage()

        self.effective_user = FakeUser()



class FakeContext:
    pass



@pytest.mark.asyncio
async def test_message_handler_basic():

    update = FakeUpdate()

    context = FakeContext()


    await handle_message(
        update,
        context,
    )


    assert len(
        update.message.responses
    ) == 1


    assert update.message.responses[0]



@pytest.mark.asyncio
async def test_empty_message_ignored():

    update = FakeUpdate()

    update.message.text = ""


    context = FakeContext()


    await handle_message(
        update,
        context,
    )


    assert (
        len(update.message.responses)
        ==
        0
    )