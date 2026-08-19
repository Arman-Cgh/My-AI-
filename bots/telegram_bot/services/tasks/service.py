from services.tasks.manager import TaskManager
from services.tasks.parser import TaskParser
from services.tasks.reminder import ReminderEngine


class TaskService:

    @staticmethod
    def create(
        user_id: int,
        message: str,
    ):

        if not message or not message.strip():

            raise ValueError(
                "متن یادآوری خالی است"
            )

        data = TaskParser.parse(
            message
        )

        if not isinstance(data, dict):

            raise ValueError(
                "اطلاعات یادآوری قابل تشخیص نیست"
            )

        title = data.get(
            "title"
        )

        if (
            not title
            or not isinstance(title, str)
            or not title.strip()
            or len(title.strip()) < 3
        ):

            raise ValueError(
                "عنوان یادآوری معتبر نیست"
            )

        due_date = data.get(
            "due_date"
        )

        due_time = data.get(
            "due_time"
        )

        if due_date and due_time:

            final_due_date = (
                f"{due_date} {due_time}"
            )

        else:

            final_due_date = due_date

        task_id = TaskManager.create(
            user_id=user_id,
            title=title.strip(),
            description="",
            due_date=final_due_date,
        )

        return {
            "id": task_id,
            "title": title.strip(),
            "due_date": final_due_date,
        }


    @staticmethod
    def get_pending(
        user_id: int,
    ):

        return TaskManager.get_pending(
            user_id
        )


    @staticmethod
    def get_all(
        user_id: int,
    ):

        return TaskManager.get_all(
            user_id
        )


    @staticmethod
    def get_due(
        user_id: int,
    ):

        return ReminderEngine.get_due_tasks(
            user_id
        )


    @staticmethod
    def complete(
        task_id: int,
        user_id: int,
    ):

        return TaskManager.complete(
            task_id,
            user_id,
        )


    @staticmethod
    def delete(
        task_id: int,
        user_id: int,
    ):

        return TaskManager.delete(
            task_id,
            user_id,
        )