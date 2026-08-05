from services.tasks.router import TaskRouter



class IntentRouter:


    @staticmethod
    def detect(message: str):


        task_intent = TaskRouter.detect(
            message
        )


        if task_intent:

            return task_intent


        return {
            "intent": "chat"
        }