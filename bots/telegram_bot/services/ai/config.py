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
# AI Provider
# ==========================

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "groq"
)


# ==========================
# API Keys
# ==========================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    ""
)


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)


# ==========================
# Base URLs
# ==========================

GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1"
)


OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1"
)


# ==========================
# Models
# ==========================

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "deepseek/deepseek-chat-v3.1"
)


# ==========================
# Backward Compatibility
# ==========================

AI_API_KEY = GROQ_API_KEY

AI_BASE_URL = GROQ_BASE_URL

AI_MODEL = GROQ_MODEL


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

MAX_TOKENS = 1200

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
از اطلاعات حافظه استفاده کن.
اگر چیزی را نمی‌دانی حدس نزن.
خروجی Plain Text باشد.
از Markdown استفاده نکن.

"""