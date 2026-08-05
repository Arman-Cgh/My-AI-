from telegram import Update
from telegram.ext import ContextTypes

from services.ai.engine import AIEngine
from database.db import save_message


ai_engine = AIEngine()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    user_id = update.effective_user.id

    user_message = update.message.text


    if not user_message:
        return


    print(
        "LOCAL BOT RECEIVED:",
        user_message
    )


    # ذخیره پیام کاربر
    try:

        save_message(
            user_id,
            "user",
            user_message
        )

    except Exception as e:

        print(
            "SAVE USER ERROR:",
            e
        )


    # دریافت پاسخ AI
    response = await ai_engine.ask(
        user_id,
        user_message
    )


    # ذخیره پاسخ AI
    try:

        save_message(
            user_id,
            "assistant",
            response
        )

    except Exception as e:

        print(
            "SAVE AI ERROR:",
            e
        )


    await update.message.reply_text(
        response
    )