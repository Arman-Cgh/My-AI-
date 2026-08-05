from datetime import datetime

from services.tasks.manager import TaskManager



class ReminderEngine:


    @staticmethod
    def get_due_tasks(user_id: int):

        tasks = TaskManager.get_all(
            user_id
        )


        today = datetime.now().date()


        due_tasks = []


        for task in tasks:

            task_id, title, description, due_date, status, created_at = task


            if status != "pending":
                continue


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

                due_tasks.append(
                    {
                        "id": task_id,
                        "title": title,
                        "due_date": due_date
                    }
                )


        return due_tasks