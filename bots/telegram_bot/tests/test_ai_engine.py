import pytest

from services.ai.engine import AIEngine


class FakeProviderManager:

    async def initialize(self):
        pass


    async def generate(
        self,
        messages,
        intent=None,
    ):

        return {
            "text": "سلام، تست موفق بود",
            "provider": "fake",
        }


@pytest.mark.asyncio
async def test_ai_engine_chat():

    engine = AIEngine()

    engine.provider_manager = FakeProviderManager()

    engine.response_pipeline.provider_manager = (
        engine.provider_manager
    )

    result = await engine.generate_response(
        user_id=12345,
        message="سلام",
        intent={
            "intent": "chat"
        },
        use_cache=False,
        extract_info=False,
    )

    assert result is not None

    assert (
        result["response"]
        == "سلام، تست موفق بود"
    )

    assert (
        result["provider"]
        == "fake"
    )