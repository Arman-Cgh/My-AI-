from services.ai.intents import IntentResult
from services.tasks.router import TaskRouter


class IntentRouter:

    @staticmethod
    def detect(message: str) -> IntentResult:

        if not message:
            return IntentResult(
                intent="chat",
                confidence=0.0,
                source="default",
            )

        task_result = TaskRouter.detect(message)

        if task_result:
            return IntentResult(
                intent="task",
                confidence=task_result.get("confidence", 0.95),
                source="task_router",
            )

        text = message.lower().strip()

        memory_keywords = (
            "یادم باشه",
            "یادت باشه",
            "یاد بگیر",
            "ذخیره کن",
            "به خاطر بسپار",
            "فراموش نکن",
            "اسم من",
            "نام من",
            "من کی هستم",
            "remember",
            "save this",
            "remember this",
            "my name",
        )

        for keyword in memory_keywords:
            if keyword in text:
                return IntentResult(
                    intent="memory",
                    confidence=0.90,
                    source="keyword",
                )

        code_keywords = (
            "کد",
            "کدنویسی",
            "پایتون",
            "ارور",
            "خطا",
            "باگ",
            "تابع",
            "کلاس",
            "python",
            "code",
            "error",
            "bug",
            "function",
            "class",
        )

        for keyword in code_keywords:
            if keyword in text:
                return IntentResult(
                    intent="code",
                    confidence=0.85,
                    source="keyword",
                )

        return IntentResult(
            intent="chat",
            confidence=0.50,
            source="default",
        )