from datetime import datetime

from services.tasks.manager import TaskManager



class ReminderEngine:



    @staticmethod
    def get_due_tasks(
        user_id: int
    ):


        tasks = TaskManager.get_pending(
            user_id
        )


        now = datetime.now()


        due_tasks = []



        for task in tasks:


            due_date = (

                task.get("due_date")
                or ""

            ).strip()



            if not due_date:

                continue



            target = None



            # ==========================
            # Full datetime
            #
            # 2026-08-08 00:40
            # ==========================

            try:

                target = datetime.strptime(

                    due_date,

                    "%Y-%m-%d %H:%M"

                )


            except ValueError:

                pass



            # ==========================
            # Date only
            #
            # Old tasks support
            # ==========================

            if target is None:


                try:

                    target = datetime.strptime(

                        due_date,

                        "%Y-%m-%d"

                    )


                except ValueError:


                    continue




            # ==========================
            # Check due
            # ==========================

            if target <= now:


                due_tasks.append(
                    task
                )



        return due_tasks

