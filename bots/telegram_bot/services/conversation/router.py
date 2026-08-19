from services.conversation.planner import ConversationPlanner


class ConversationRouter:

    def __init__(
        self,
        planner=None,
    ):

        self.planner = (
            planner
            or ConversationPlanner()
        )

    def route(
        self,
        intent,
    ):

        plan = self.planner.create_plan(
            intent
        )

        return {
            "action": plan.action,
            "intent": plan.intent,
            "requires_ai": plan.requires_ai,
            "save_history": plan.save_history,
        }