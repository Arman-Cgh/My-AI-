from telegram import Update
from telegram.ext import ContextTypes

from config import BOT_NAME, BOT_CREATOR
from database.db import add_user, create_referral
from handlers.user_callbacks import get_main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    if context.args:
        payload = context.args[0]
        if payload.startswith("ref_"):
            try:
                inviter_id = int(payload.split("_", 1)[1])
                create_referral(inviter_id, user.id)
            except ValueError:
                pass

    await update.message.reply_text(
        f"👋 سلام {user.first_name}!\n\n"
        f"به {BOT_NAME} خوش آمدید 🤖\n\n"
        "من دستیار هوش مصنوعی شما هستم.\n\n"
        f"Made by: {BOT_CREATOR}",
        reply_markup=get_main_keyboard()
    )