class ModelRouter:


    MODELS = {

        "chat": "deepseek/deepseek-chat-v3.1",

        "code": "deepseek/deepseek-coder",

        "memory": "deepseek/deepseek-chat-v3.1",

        "task": None,

        "vision": "google/gemini-2.5-flash"

    }



    @classmethod
    def select(
        cls,
        provider_name,
        intent
    ):

        return cls.MODELS.get(
            intent,
            cls.MODELS["chat"]
        )