import sys
import os

# Ensure project package path is available for imports
ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_BOT_PATH = os.path.join(ROOT, 'bots', 'telegram_bot')
if PROJECT_BOT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_BOT_PATH)

from services.ai.extraction_router import ExtractionRouter


def run_case(intent, user_message, assistant_response=""):
    res = ExtractionRouter.should_extract(intent, user_message, assistant_response)
    print(f"intent={intent!r}, message={ascii(user_message)} -> {res}")
    return res


# Expected True cases
assert run_case("memory", "anything") is True
assert run_case("chat", "یادت باشه اسم من یونس است") is True
assert run_case("chat", "به خاطر بسپار که من برنامه نویس هستم") is True
assert run_case("chat", "remember my name") is True
assert run_case("chat", "call me Alex") is True
assert run_case("chat", "please save this") is True

# Expected False cases
assert run_case("code", "چطور در پایتون کلاس بسازم") is False
assert run_case("chat", "سلام") is False
assert run_case("chat", "مرسی") is False
assert run_case("chat", "امروز هوا چطوره") is False

print("All extraction_router tests passed.")
