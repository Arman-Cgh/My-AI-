from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes


ADMIN_ID = 5383969883


async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "⛔ دسترسی ندارید."
        )

        return


    keyboard = [

        [
            InlineKeyboardButton(
                "👥 کاربران",
                callback_data="users"
            ),

            InlineKeyboardButton(
                "💳 اشتراک‌ها",
                callback_data="subscription"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 آمار",
                callback_data="stats"
            ),
 
            InlineKeyboardButton(
                "📢 پیام همگانی",
                callback_data="broadcast"
            )
        ],
 
        [
            InlineKeyboardButton(
                "💰 قیمت‌ها",
                callback_data="pricing"
            ),
 
            InlineKeyboardButton(
                "👥 رفرال",
                callback_data="referral_settings"
            )
        ],
 
        [
            InlineKeyboardButton(
                "🖼 ساخت عکس",
                callback_data="image"
            ),
 
            InlineKeyboardButton(
                "🧠 دانش فنی",
                callback_data="technical"
            )
        ],

        [
            InlineKeyboardButton(
                "🚫 بن کاربر",
                callback_data="ban_user"
            ),

            InlineKeyboardButton(
                "❌ بستن",
                callback_data="close"
            )
        ]

    ]


    await update.message.reply_text(

        "🛠 پنل مدیریت PF-Ai",

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )

    )