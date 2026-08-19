from telegram import Update
from telegram.ext import ContextTypes

from services.tasks.service import TaskService



async def done_task(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    if not update.effective_user:
        return


    user_id = update.effective_user.id


    if not context.args:

        await update.message.reply_text(
            "استفاده:\n/done task_id"
        )

        return


    try:

        task_id = int(
            context.args[0]
        )


    except ValueError:

        await update.message.reply_text(
            "شناسه نامعتبر است"
        )

        return



    success = TaskService.complete(
        task_id,
        user_id
    )



    if success:

        await update.message.reply_text(
            "✅ یادآوری انجام شد"
        )

    else:

        await update.message.reply_text(
            "❌ یادآوری پیدا نشد یا دسترسی ندارید"
        )





async def delete_task(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    if not update.effective_user:
        return


    user_id = update.effective_user.id



    if not context.args:

        await update.message.reply_text(
            "استفاده:\n/delete task_id"
        )

        return



    try:

        task_id = int(
            context.args[0]
        )


    except ValueError:

        await update.message.reply_text(
            "شناسه نامعتبر است"
        )

        return



    success = TaskService.delete(
        task_id,
        user_id
    )



    if success:

        await update.message.reply_text(
            "🗑 یادآوری حذف شد"
        )

    else:

        await update.message.reply_text(
            "❌ یادآوری پیدا نشد یا دسترسی ندارید"
        )