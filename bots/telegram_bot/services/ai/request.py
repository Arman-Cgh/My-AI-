from services.ai.intent_router import IntentRouter



class AIRequest:



    def __init__(

        self,

        user_id: int,

        message: str

    ):


        self.user_id = user_id

        self.message = message

        self.result = None



    def analyze(self):


        self.result = IntentRouter.detect(

            self.message

        )


        return self



    @property
    def intent(self):

        return self.result.intent



    @property
    def confidence(self):

        return self.result.confidence



    def data(self):

        return {

            "user_id": self.user_id,

            "message": self.message,

            "intent": self.intent,

            "confidence": self.confidence,

            "source": self.result.source

        }