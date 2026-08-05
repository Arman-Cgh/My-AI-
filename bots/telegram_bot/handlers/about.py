from telegram import Update
from telegram.ext import ContextTypes


async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        """
🤖 PF-AI

یک دستیار هوشمند شخصی با قابلیت:

🧠 حافظه بلندمدت
💬 گفتگو هوشمند
👤 شناخت کاربر
🐍 ساخته شده با Python

Developer:
@whocareit
"""
    )