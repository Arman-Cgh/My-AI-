import pytest

from services.ai.extractor import extract_memory


class FakeProvider:

    async def generate(
        self,
        messages,
        model=None
    ):

        return """
        {
            "memory": {
                "name": "یونس",
                "job": "برنامه نویس پایتون",
                "random": "delete"
            },
            "state": {
                "active_project": "PFAST_AI"
            }
        }
        """


@pytest.mark.asyncio
async def test_memory_extraction():

    result = await extract_memory(
        provider=FakeProvider(),
        provider_name="fake",
        user_id=1,
        user_message="اسم من یونس است",
        assistant_response="باشه"
    )


    assert result["memory"]["name"] == "یونس"

    assert (
        result["memory"]["job"]
        ==
        "برنامه نویس پایتون"
    )

    assert (
        "random"
        not in result["memory"]
    )


    assert (
        result["state"]["active_project"]
        ==
        "PFAST_AI"
    )