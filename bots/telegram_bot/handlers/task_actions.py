from telegram import Update
from telegram.ext import ContextTypes

from services.tasks.manager import TaskManager



async def done_task(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
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

    except:

        await update.message.reply_text(
            "شناسه نامعتبر است"
        )

        return



    TaskManager.complete(
        task_id,
        user_id
    )


    await update.message.reply_text(
        "✅ یادآوری انجام شد"
    )





async def delete_task(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
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

    except:

        await update.message.reply_text(
            "شناسه نامعتبر است"
        )

        return



    TaskManager.delete(
        task_id,
        user_id
    )


    await update.message.reply_text(
        "🗑 یادآوری حذف شد"
    )