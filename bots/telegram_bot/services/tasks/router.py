class TaskRouter:


    @staticmethod
    def detect(message: str):

        if not message:
            return None


        text = message.lower()


        triggers = [
            "یادم بنداز",
            "یادآوری",
            "یادآور",
            "remind",
            "reminder"
        ]


        for word in triggers:

            if word in text:

                return {
                    "intent": "create_task"
                }


        return None