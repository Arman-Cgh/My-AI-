from datetime import datetime

from services.tasks.manager import TaskManager



class ReminderEngine:



    @staticmethod
    def get_due_tasks(
        user_id:int
    ):


        tasks = TaskManager.get_pending(
            user_id
        )


        today = datetime.now().date()


        result = []



        for task in tasks:


            due_date = task.get(
                "due_date"
            )


            if not due_date:

                continue



            try:

                task_date = datetime.strptime(

                    due_date[:10],

                    "%Y-%m-%d"

                ).date()



            except Exception:

                continue



            if task_date <= today:


                result.append(
                    task
                )



        return result