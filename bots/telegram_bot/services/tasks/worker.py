import asyncio

from services.tasks.reminder import ReminderEngine
from services.tasks.manager import TaskManager



class TaskWorker:


    def __init__(
        self,
        bot
    ):

        self.bot = bot
        self.running = True



    async def start(self):

        print(
            "TASK WORKER STARTED"
        )


        while self.running:

            try:

                await self.check_tasks()


            except Exception as e:

                print(
                    "WORKER ERROR:",
                    e
                )


            await asyncio.sleep(
                60
            )



    async def check_tasks(self):

        from database.db import get_all_users


        users = get_all_users()


        for user_id in users:


            tasks = ReminderEngine.get_due_tasks(
                user_id
            )


            for task in tasks:


                try:

                    await self.bot.send_message(

                        chat_id=user_id,

                        text=(
                            "⏰ یادآوری\n\n"
                            f"📝 {task['title']}\n"
                            f"📅 {task['due_date']}"
                        )

                    )


                    TaskManager.complete(

                        task["id"],

                        user_id

                    )


                except Exception as e:

                    print(
                        "SEND REMINDER ERROR:",
                        e
                    )   