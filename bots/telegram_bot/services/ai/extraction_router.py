class ExtractionRouter:

    @staticmethod
    def should_extract(intent, user_message, assistant_response) -> bool:
        """
        Decide whether memory extraction should run.

        Rules:
        1. Always extract: intent == "memory"
        2. Never extract: intent == "task" or intent == "code"
        3. For chat: extract only when user_message or assistant_response contains memory signals
        """

        intent = (intent or "").strip().lower()
        user_message = (user_message or "").strip().lower()
        assistant_response = (assistant_response or "").strip().lower()

        # Always extract for explicit memory intent
        if intent == "memory":
            return True

        # Never extract for these intents
        if intent in ("task", "code"):
            return False

        # Only consider signals for chat-like intents
        # Define signal keywords/phrases (English + Persian)
        signals = [
            # English
            "remember",
            "save this",
            "my name",
            "call me",
            "i am ",
            "i'm ",
            # Persian
            "یادت باشه",
            "به خاطر بشپار",
            "به خاطر بسپار",
            "ذخیره کن",
            "اسم من",
            "من هستم",
            "پروژه من",
            "هدف من",
            # variations
            "yadet",
            "yadet bashe",
        ]

        # Check both user message and assistant response for any signal
        combined = user_message + "\n" + assistant_response

        for kw in signals:
            if kw in combined:
                return True

        return False
