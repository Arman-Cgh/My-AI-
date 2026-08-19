import pytest

from services.ai.pipeline.memory import MemoryPipeline


def test_memory_keyword_detection():

    assert MemoryPipeline.should_extract(
        intent="chat",
        message="یادت باشه اسم من یونس است"
    )


def test_memory_skip_code():

    assert not MemoryPipeline.should_extract(
        intent="code",
        message="یادت باشه این کد را ذخیره کن"
    )


def test_memory_skip_normal_chat():

    assert not MemoryPipeline.should_extract(
        intent="chat",
        message="امروز هوا چطوره؟"
    )