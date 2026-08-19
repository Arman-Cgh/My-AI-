from telegram import Update
from telegram.ext import ContextTypes

from services.tasks.service import TaskService



async def tasks_command(
    update:Update,
    context:ContextTypes.DEFAULT_TYPE
):


    if not update.message:

        return



    user_id=update.effective_user.id



    tasks=TaskService.get_pending(
        user_id
    )



    if not tasks:


        await update.message.reply_text(

            "📋 شما هیچ یادآوری فعالی ندارید."

        )

        return



    text="📋 یادآوری‌های فعال شما:\n\n"



    for index,task in enumerate(tasks,start=1):


        text += (

            f"{index}) {task['title']}\n"

            f"📅 {task.get('due_date') or 'بدون تاریخ'}\n"

            f"🆔 {task['id']}\n\n"

        )



    await update.message.reply_text(text)