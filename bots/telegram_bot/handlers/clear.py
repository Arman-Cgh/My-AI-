from telegram import Update
from telegram.ext import ContextTypes

from database.db import clear_user_memory


async def clear_memory(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    clear_user_memory(
        user_id
    )


    await update.message.reply_text(
        "🧹 حافظه من از اطلاعات ذخیره شده شما پاک شد."
    )