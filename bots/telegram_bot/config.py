import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

AI_API_KEY = os.getenv("AI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", AI_API_KEY)
TOKENFAUCET_API_KEY = os.getenv("TOKENFAUCET_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", TELEGRAM_TOKEN)
BOT_NAME = os.getenv("BOT_NAME", "PF-AI")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
BOT_CREATOR = os.getenv("BOT_CREATOR", "@whocareit")