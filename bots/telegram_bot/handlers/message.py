from telegram import Update
from telegram.ext import ContextTypes

from services.ai.engine import AIEngine
from services.tasks.service import TaskService

from database.db import (
    save_message,
    get_admin_action,
    clear_admin_action,
    set_plan_price,
    set_referral_settings,
)

from database.plans import update_plan
from handlers.admin_callbacks import ADMIN_ID


from utils.permissions import check_and_consume_feature



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



    # ==========================
    # Save User Message
    # ==========================

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



    # ==========================
    # Admin Actions
    # ==========================

    try:

        if user_id == ADMIN_ID:


            action = get_admin_action(
                user_id
            )


            if action:


                # ------------------
                # Set Plan Price
                # ------------------

                if action.startswith(
                    "set_price:"
                ):

                    plan_name = action.split(
                        ":",
                        1
                    )[1]


                    try:

                        price = set_plan_price(
                            plan_name,
                            user_message
                        )


                        await update.message.reply_text(
                            f"✅ قیمت {plan_name.upper()} تنظیم شد\n\n{price}"
                        )


                    except Exception as e:

                        await update.message.reply_text(
                            f"❌ خطا: {e}"
                        )


                    clear_admin_action(
                        user_id
                    )

                    return



                # ------------------
                # Referral Config
                # ------------------

                if action == "set_referral_config":


                    try:

                        parts = user_message.split()


                        if len(parts) != 3:

                            raise ValueError(
                                "فرمت: invites days plan"
                            )


                        required_invites = int(
                            parts[0]
                        )

                        reward_days = int(
                            parts[1]
                        )

                        reward_plan = parts[2]


                        set_referral_settings(
                            required_invites,
                            reward_days,
                            reward_plan
                        )


                        await update.message.reply_text(
                            "✅ تنظیمات رفرال ذخیره شد"
                        )


                    except Exception as e:

                        await update.message.reply_text(
                            f"❌ خطا: {e}"
                        )


                    clear_admin_action(
                        user_id
                    )

                    return



                # ------------------
                # Edit Plan
                # ------------------

                if action.startswith(
                    "edit_plan_waiting:"
                ):


                    parts = action.split(
                        ":",
                        2
                    )


                    if len(parts) != 3:

                        await update.message.reply_text(
                            "درخواست نامعتبر"
                        )

                        clear_admin_action(
                            user_id
                        )

                        return



                    plan_name = parts[1]

                    key = parts[2]



                    success, msg = update_plan(
                        plan_name,
                        {
                            key:user_message.strip()
                        }
                    )



                    if success:

                        await update.message.reply_text(
                            "✅ پلن بروزرسانی شد"
                        )

                    else:

                        await update.message.reply_text(
                            f"❌ {msg}"
                        )



                    clear_admin_action(
                        user_id
                    )

                    return



    except Exception as e:

        print(
            "ADMIN ERROR:",
            e
        )



    # ==========================
    # Task System
    # ==========================

    try:

        task_result = TaskService.handle(
            user_id,
            user_message
        )


    except Exception as e:

        print(
            "TASK ERROR:",
            e
        )

        task_result = None



    if task_result:


        response = (
            "✅ یادآوری ثبت شد\n\n"
            f"📝 {task_result['title']}\n"
            f"📅 {task_result['due_date'] or 'بدون تاریخ'}"
        )


        save_message(
            user_id,
            "assistant",
            response
        )


        await update.message.reply_text(
            response
        )


        return



    # ==========================
    # Pending Actions
    # ==========================


    pending = context.user_data.get(
        "pending_action"
    )



    # --------------------------
    # Technical Question
    # --------------------------

    if pending == "tech":


        allowed = check_and_consume_feature(
            user_id,
            "technical",
            amount=1
        )


        if not allowed:

            await update.message.reply_text(
                "⚠️ محدودیت سوال فنی امروز تمام شده است"
            )

            context.user_data.pop(
                "pending_action",
                None
            )

            return



        try:

            response = await ai_engine.ask(
                user_id,
                f"سوال فنی: {user_message}"
            )


            save_message(
                user_id,
                "assistant",
                response
            )


            await update.message.reply_text(
                response
            )


        except Exception as e:

            print(
                "TECH ERROR:",
                e
            )

            await update.message.reply_text(
                "❌ خطا در پاسخ فنی"
            )


        context.user_data.pop(
            "pending_action",
            None
        )


        return




    # --------------------------
    # Image
    # --------------------------

    if pending == "image":


        allowed = check_and_consume_feature(
            user_id,
            "image",
            amount=1
        )


        if not allowed:

            await update.message.reply_text(
                "⚠️ محدودیت تصویر امروز تمام شده است"
            )

            context.user_data.pop(
                "pending_action",
                None
            )

            return



        image_url = (
            "https://example.com/generated_image.png"
        )


        response = (
            f"🖼 تصویر ساخته شد:\n{image_url}"
        )


        save_message(
            user_id,
            "assistant",
            response
        )


        await update.message.reply_text(
            response
        )


        context.user_data.pop(
            "pending_action",
            None
        )


        return




    # ==========================
    # Normal AI Chat
    # ==========================


    allowed = check_and_consume_feature(
        user_id,
        "chat",
        amount=1
    )



    if not allowed:

        await update.message.reply_text(
            "⚠️ محدودیت روزانه شما تمام شده است"
        )

        return



    try:

        response = await ai_engine.ask(
            user_id,
            user_message
        )


        save_message(
            user_id,
            "assistant",
            response
        )


        await update.message.reply_text(
            response
        )



    except Exception as e:

        print(
            "AI HANDLER ERROR:",
            e
        )


        await update.message.reply_text(
            "❌ مشکلی در پردازش درخواست پیش آمد."
        )