import logging

from telegram import Update
from telegram.ext import ContextTypes

from database.db import (
    add_user,
    is_user_banned,
)

from services.conversation.handler import ConversationHandler


logger = logging.getLogger(__name__)


conversation_handler = ConversationHandler()


def clean_ai_response(
    text: str,
) -> str:

    if not text:
        return ""

    text = str(text)

    text = text.replace(
        "**",
        "",
    )

    text = text.replace(
        "__",
        "",
    )

    text = text.replace(
        "`",
        "",
    )

    return text.strip()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    user = update.effective_user

    if not user:
        return

    user_id = user.id

    text = (
        update.message.text
        or ""
    ).strip()

    if not text:
        return

    add_user(
        user_id,
        user.username or "",
        user.first_name or "",
    )

    if is_user_banned(user_id):

        await update.message.reply_text(
            "دسترسی شما محدود شده است."
        )

        return

    try:

        response = await conversation_handler.handle(
            user_id=user_id,
            message=text,
        )

        response = clean_ai_response(
            response,
        )

        if not response:

            response = (
                "متاسفانه پاسخی دریافت نشد."
            )

        await update.message.reply_text(
            response,
        )

    except Exception:

        logger.exception(
            "Message processing failed",
        )

        await update.message.reply_text(
            "❌ مشکلی در پردازش درخواست پیش آمد.",
        )