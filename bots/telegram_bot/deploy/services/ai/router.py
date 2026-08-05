from services.ai.config import AI_MODEL


def select_model(
    task: str = "chat"
):

    models = {

        "chat": AI_MODEL,

        "memory": AI_MODEL,

        "code": AI_MODEL

    }


    return models.get(
        task,
        AI_MODEL
    )