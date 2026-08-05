from telegram import Update
from telegram.ext import ContextTypes

from config import BOT_NAME
from handlers.user_callbacks import get_main_keyboard


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"🤖 راهنمای {BOT_NAME}\n\n"
        "/start - شروع ربات\n"
        "/help - راهنما\n"
        "/plan - مشاهده وضعیت اشتراک و محدودیت‌ها\n"
        "/buy - خرید یا ارتقا اشتراک\n"
        "/referral - کد دعوت و رفرال\n"
        "/image <متن> - ساخت تصویر با هوش مصنوعی\n"
        "/tech <سوال فنی> - پاسخ به سوال‌های فنی\n"
        "/profile - مشاهده اطلاعات ذخیره شده شما",
        reply_markup=get_main_keyboard()
    )