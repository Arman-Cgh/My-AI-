from telegram import Update
from telegram.ext import ContextTypes

from services.ai.engine import AIEngine
from database.db import save_message
from utils.permissions import check_and_consume_feature
from core.logger import logger


async def tech_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    question = " ".join(context.args).strip()

    if not question:
        await update.message.reply_text(
            "🧠 برای سوال فنی از دستور زیر استفاده کن:\n"
            "/tech <سوال فنی>"
        )
        return

    # Permission + atomic consume
    allowed = check_and_consume_feature(user_id, 'technical', amount=1)
    if not allowed:
        await update.message.reply_text(
            "⚠️ محدودیت سوال‌های فنی امروز شما تمام شده است.\n"
            "برای دسترسی بیشتر، اشتراک خود را ارتقا دهید."
        )
        return

    save_message(user_id, "user", f"/tech {question}")

    try:
        response = await AIEngine().ask(
            user_id=user_id,
            user_message=f"سوال فنی: {question}"
        )
        save_message(user_id, "assistant", response)
        await update.message.reply_text(response)
    except Exception as error:
        logger.error(
            f"TECH COMMAND ERROR: {error}"
        )
        await update.message.reply_text(
            "متاسفانه در پاسخ به سوال فنی مشکلی پیش آمد."
        )
