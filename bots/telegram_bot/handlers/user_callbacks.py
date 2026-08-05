from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import BOT_NAME
from database.db import create_payment_request, get_plan_prices, get_referral_link, get_referral_settings
from handlers.plan import build_plan_text
from handlers.profile import build_profile_text


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_plan_prices()
    text = "💳 پلن‌های قابل خرید:\n\n"
    for plan_name, plan_data in prices.items():
        if plan_name == "free":
            continue
        text += f"• {plan_name.upper()}: {plan_data['price']} {plan_data['currency']}\n"

    await update.message.reply_text(
        text,
        reply_markup=build_buy_keyboard(prices)
    )


async def referral_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referral_link = get_referral_link(update.effective_user.id)
    await update.message.reply_text(
        "👥 کد دعوت شما:\n"
        f"{referral_link}\n\n"
        "هر کاربری که با این لینک وارد شود، به عنوان دعوت‌شده ثبت می‌شود."
    )


async def user_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if data == "feature:image":
        context.user_data["pending_action"] = "image"
        await query.edit_message_text(
            "🖼 متن تصویر را بفرست تا برایت بسازم."
        )
        return

    if data == "feature:tech":
        context.user_data["pending_action"] = "tech"
        await query.edit_message_text(
            "🧠 سوال فنی‌ات را بفرست تا پاسخ بدهم."
        )
        return

    if data == "feature:profile":
        await query.edit_message_text(
            build_profile_text(user_id)
        )
        return

    if data == "feature:plan":
        await query.edit_message_text(
            build_plan_text(user_id)
        )
        return

    if data == "feature:buy_subscription":
        prices = get_plan_prices()
        keyboard = build_buy_keyboard(prices)
        text = "💳 پلن‌های قابل خرید:\n\n"
        for plan_name, data in prices.items():
            if plan_name == "free":
                continue
            price = data["price"]
            currency = data["currency"]
            text += f"• {plan_name.upper()}: {price} {currency}\n"

        text += "\nبرای خرید مستقیم، روی پلن موردنظر بزن."
        await query.edit_message_text(text, reply_markup=keyboard)
        return

    if data.startswith("buy:"):
        plan_name = data.split(":", 1)[1]
        prices = get_plan_prices()
        plan_data = prices.get(plan_name, {"price": 0, "currency": "IRR"})
        request_id = create_payment_request(
            user_id,
            plan_name,
            plan_data["price"],
            plan_data["currency"],
            30
        )
        settings = get_referral_settings()
        await query.edit_message_text(
            f"💳 درخواست پرداخت برای پلن {plan_name.upper()} ایجاد شد.\n"
            f"شناسه درخواست: {request_id}\n"
            f"مبلغ: {plan_data['price']} {plan_data['currency']}\n"
            f"مدت: 30 روز\n\n"
            "در مرحله بعد این درخواست به درگاه واقعی متصل می‌شود."
            f"\n\nبرای کاربرهای دعوت‌شده، پس از {settings['required_invites']} دعوت، جایزه {settings['reward_days']} روزه برای پلن {settings['reward_plan'].upper()} فعال می‌شود."
        )
        return

    if data == "feature:referral":
        referral_link = get_referral_link(user_id)
        await query.edit_message_text(
            "👥 کد دعوت شما:\n"
            f"{referral_link}\n\n"
            "هر کاربری که با این لینک وارد شود، به عنوان دعوت‌شده ثبت می‌شود و پس از رسیدن به حد نصاب، برای شما جایزه اشتراک فعال می‌شود."
        )
        return

    if data == "feature:help":
        await query.edit_message_text(
            f"🤖 راهنمای {BOT_NAME}\n\n"
            "• /start - بازگشت به منو\n"
            "• /image <متن> - ساخت تصویر\n"
            "• /tech <سوال فنی> - پاسخ فنی\n"
            "• /plan - وضعیت اشتراک"
        )
        return

    await query.edit_message_text(
        "در حال توسعه..."
    )



def build_buy_keyboard(prices):
    buttons = []
    for plan_name in ["pro", "ultra"]:
        plan_data = prices.get(plan_name, {"price": 0, "currency": "IRR"})
        label = f"{plan_name.upper()} - {plan_data['price']} {plan_data['currency']}"
        buttons.append(
            InlineKeyboardButton(label, callback_data=f"buy:{plan_name}")
        )

    buttons.append(InlineKeyboardButton("↩️ بازگشت", callback_data="feature:plan"))
    return InlineKeyboardMarkup([buttons])


def get_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🖼 ساخت عکس",
                callback_data="feature:image"
            ),
            InlineKeyboardButton(
                "🧠 دانش فنی",
                callback_data="feature:tech"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 اطلاعات من",
                callback_data="feature:profile"
            ),
            InlineKeyboardButton(
                "📦 اشتراک/پلن",
                callback_data="feature:plan"
            )
        ],
        [
            InlineKeyboardButton(
                "💳 خرید اشتراک",
                callback_data="feature:buy_subscription"
            ),
            InlineKeyboardButton(
                "👥 دعوت دوستان",
                callback_data="feature:referral"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ راهنما",
                callback_data="feature:help"
            )
        ]
    ])
