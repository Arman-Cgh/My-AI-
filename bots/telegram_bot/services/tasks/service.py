from services.tasks.parser import TaskParser
from services.tasks.manager import TaskManager
from services.tasks.reminder import ReminderEngine



class TaskService:



    @staticmethod
    def handle(
        user_id:int,
        message:str
    ):


        intent_words = [

            "یادم بنداز",

            "یادآوری",

            "یادآوری کن",

            "remind",

            "task",

            "وظیفه",

            "کار دارم"

        ]


        text = message.lower()


        is_task = False


        for word in intent_words:

            if word in text:

                is_task = True
                break



        if not is_task:

            return None



        data = TaskParser.parse(
            message
        )



        task_id = TaskManager.create(

            user_id=user_id,

            title=data["title"],

            description="",

            due_date=data["due_date"]

        )



        return {

            "id": task_id,

            "title": data["title"],

            "due_date": data["due_date"]

        }




    @staticmethod
    def get_pending(
        user_id:int
    ):

        return TaskManager.get_pending(
            user_id
        )




    @staticmethod
    def get_due(
        user_id:int
    ):

        return ReminderEngine.get_due_tasks(
            user_id
        )




    @staticmethod
    def complete(
        task_id:int,
        user_id:int
    ):

        return TaskManager.complete(
            task_id,
            user_id
        )




    @staticmethod
    def delete(
        task_id:int,
        user_id:int
    ):

        return TaskManager.delete(
            task_id,
            user_id
        )