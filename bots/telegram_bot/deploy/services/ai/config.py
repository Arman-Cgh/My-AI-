import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env"
    )
)


# ==========================
# AI
# ==========================

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "openrouter"
)


AI_API_KEY = os.getenv(
    "AI_API_KEY",
    ""
)


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)


AI_BASE_URL = os.getenv(
    "AI_BASE_URL",
    "https://openrouter.ai/api/v1"
)


AI_MODEL = os.getenv(
    "AI_MODEL",
    "google/gemma-4-26b-a4b-it:free"
)



# ==========================
# Telegram
# ==========================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)



# ==========================
# Bot
# ==========================

BOT_NAME = os.getenv(
    "BOT_NAME",
    "PF-AI"
)


BOT_CREATOR = os.getenv(
    "BOT_CREATOR",
    "@whocareit"
)



# ==========================
# AI Settings
# ==========================

MAX_TOKENS = 800

TEMPERATURE = 0.8

SHORT_MEMORY_LIMIT = 20

LONG_MEMORY_ENABLED = True



# ==========================
# Personality
# ==========================

SYSTEM_PROMPT = """

تو PF-AI هستی.

یک دستیار هوشمند شخصی.

همیشه فارسی روان صحبت کن.
خودت را PF-AI معرفی کن.
از اطلاعات حافظه استفاده کن.
اگر اطلاعاتی را نمی‌دانی، حدس نزن.
خروجی Plain Text باشد.
از Markdown استفاده نکن.

"""