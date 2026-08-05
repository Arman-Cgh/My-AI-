from telegram import Update
from telegram.ext import ContextTypes

from services.tasks.manager import TaskManager



async def tasks_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    user_id = update.effective_user.id


    tasks = TaskManager.get_all(
        user_id
    )


    pending_tasks = []


    for task in tasks:

        task_id, title, description, due_date, status, created_at = task


        if status == "pending":

            pending_tasks.append(
                {
                    "id": task_id,
                    "title": title,
                    "due_date": due_date
                }
            )



    if not pending_tasks:

        await update.message.reply_text(
            "📋 شما هیچ یادآوری فعالی ندارید."
        )

        return



    text = "📋 یادآوری‌های فعال شما:\n\n"


    for index, task in enumerate(
        pending_tasks,
        start=1
    ):

        text += (
            f"{index}) {task['title']}\n"
            f"📅 {task['due_date']}\n"
            f"🆔 {task['id']}\n\n"
        )



    await update.message.reply_text(
        text
    )