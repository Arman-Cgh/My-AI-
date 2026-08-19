from datetime import datetime



class ConversationMiddleware:



    def __init__(
        self,
        max_message_length=4000
    ):

        self.max_message_length = max_message_length



    # ==========================
    # Before Processing
    # ==========================

    def before_process(
        self,
        user_id,
        message
    ):


        if message is None:

            return {

                "allowed": False,

                "message": "پیام خالی است."

            }



        message = str(
            message
        ).strip()



        if not message:

            return {

                "allowed": False,

                "message": "پیام خالی است."

            }



        if len(message) > self.max_message_length:


            message = (

                message[:self.max_message_length]

                +

                "..."

            )



        return {


            "allowed": True,


            "user_id": user_id,


            "message": message,


            "timestamp": datetime.now().isoformat()

        }



    # ==========================
    # After AI Response
    # ==========================

    def after_process(
        self,
        response
    ):


        if response is None:

            return "پاسخی دریافت نشد."



        response = str(
            response
        ).strip()



        if not response:

            return "پاسخی دریافت نشد."



        return response