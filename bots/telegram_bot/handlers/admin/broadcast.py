from telegram import Update
from telegram.ext import ContextTypes

from handlers.admin.state import (
    set_state,
    clear_state
)


async def start_broadcast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    user_id = query.from_user.id

    set_state(user_id, "broadcast")

    await query.edit_message_text(
        "📢 حالت ارسال همگانی فعال شد.\n\n"
        "حالا پیام موردنظر را ارسال کنید.\n\n"
        "می‌توانید متن، عکس، ویدیو، فایل، ویس، گیف یا هر نوع پیام دیگری را ارسال کنید."
    )


async def cancel_broadcast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    clear_state(user_id)

    await update.message.reply_text(
        "❌ ارسال همگانی لغو شد."
    )