import sys
import os

import pytest


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)


from services.ai.engine import AIEngine


@pytest.mark.asyncio
async def test_engine_prompt_build():

    engine = AIEngine()

    await engine.initialize()

    messages = await engine.response_pipeline.build_messages(
        user_id=1,
        message="سلام، خودتو معرفی کن",
        intent="chat",
    )

    assert isinstance(
        messages,
        list
    )

    assert len(messages) > 0

    for msg in messages:

        assert "role" in msg
        assert "content" in msg
