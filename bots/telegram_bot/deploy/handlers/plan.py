from telegram import Update
from telegram.ext import ContextTypes

from database.plans import get_user_limits, get_user_plan
from database.usage import get_usage
from database.subscriptions import get_subscription


def build_plan_text(user_id: int) -> str:
    plan_name = get_user_plan(user_id)
    limits = get_user_limits(user_id)
    usage = get_usage(user_id)
    subscription = get_subscription(user_id)

    text = (
        f"📦 طرح شما: {plan_name}\n"
        f"• پیام‌های امروز: {usage['messages']} / {limits['daily_messages']}\n"
        f"• تصاویر امروز: {usage['images']} / {limits['daily_images']}\n"
        f"• سوال‌های فنی امروز: {usage['code_requests']} / {limits.get('daily_technical_questions', 'نامحدود')}\n"
        f"• زمان انتظار بین پیام‌ها: {limits['cooldown_seconds']} ثانیه\n"
        "\n"
    )

    if subscription.get("is_active"):
        text += (
            f"🔔 اشتراک فعال است.\n"
            f"• تاریخ شروع: {subscription.get('start_date')}\n"
            f"• پایان: {subscription.get('end_date')}\n"
            f"• روزهای باقی‌مانده: {subscription.get('days_remaining')}\n"
            "\n"
        )
    elif subscription.get("status") in ["expired", "cancelled"]:
        text += (
            f"🔔 اشتراک شما {subscription.get('status')} شده است.\n"
            f"• طرح قبلی: {subscription.get('plan')}\n"
            "\n"
        )

    text += (
        "برای ارتقا به طرح‌های حرفه‌ای با ادمین تماس بگیرید.\n"
        "اگر می‌خواهید طرح را تغییر دهید، از ادمین بخواهید روی حساب شما تنظیم کند."
    )
    return text


async def plan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        build_plan_text(user_id)
    )
