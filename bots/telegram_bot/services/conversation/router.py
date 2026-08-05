from services.ai.intents import IntentResult


class ConversationRouter:


    @staticmethod
    def route(intent_result):

        if not isinstance(
            intent_result,
            IntentResult
        ):
            return "chat"



        if intent_result.intent == "task":

            return "task"



        if intent_result.intent == "memory":

            return "memory"



        if intent_result.intent == "code":

            return "code"



        return "chat"