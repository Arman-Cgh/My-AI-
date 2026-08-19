import re

from services.tasks.constants import TASK_TRIGGER_WORDS


class TaskRouter:

    # ==========================
    # Explicit Task Detection
    # ==========================

    @staticmethod
    def _detect_explicit(text: str):

        for keyword in TASK_TRIGGER_WORDS:

            if keyword.lower() in text:

                return {
                    "intent": "task",
                    "confidence": 0.95,
                    "source": "keyword",
                }

        return None

    # ==========================
    # Normalize Text
    # ==========================

    @staticmethod
    def _normalize(text: str) -> str:

        text = str(text or "").strip().lower()

        replacements = {
            "ي": "ی",
            "ى": "ی",
            "ك": "ک",
            "ۀ": "ه",
            "ة": "ه",
            "ؤ": "و",
            "إ": "ا",
            "أ": "ا",
            "ٱ": "ا",
        }

        for source, target in replacements.items():
            text = text.replace(
                source,
                target,
            )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # ==========================
    # Semantic Task Detection
    # ==========================

    @staticmethod
    def _detect_semantic(text: str):

        temporal_patterns = (
            r"\bامروز\b",
            r"\bفردا\b",
            r"\bپس\s*فردا\b",
            r"\bپسفردا\b",
            r"\bامشب\b",
            r"\bصبح\b",
            r"\bظهر\b",
            r"\bعصر\b",
            r"\bشب\b",
            r"\bساعت\s+\d{1,2}",
            r"\b\d+\s*دقیقه\s*(?:دیگه|دیگر|بعد)",
            r"\b\d+\s*ساعت\s*(?:دیگه|دیگر|بعد)",
        )

        has_time = any(
            re.search(
                pattern,
                text,
            )
            for pattern in temporal_patterns
        )

        if not has_time:
            return None

        action_patterns = (
            r"\bبررسی\s+کن\b",
            r"\bانجام\s+بده\b",
            r"\bانجامش\s+بده\b",
            r"\bپیگیری\s+کن\b",
            r"\bیادآوری\s+کن\b",
            r"\bیادآوریش\s+کن\b",
            r"\bیادم\s+بنداز\b",
            r"\bیادآوری\s+بده\b",
            r"\bزنگ\s+بزن\b",
            r"\bتماس\s+بگیر\b",
            r"\bپیام\s+بده\b",
            r"\bپیام\s+بفرست\b",
            r"\bبنویس\b",
            r"\bبفرست\b",
            r"\bارسال\s+کن\b",
            r"\bآماده\s+کن\b",
            r"\bتکمیل\s+کن\b",
            r"\bتمام\s+کن\b",
            r"\bcheck\b",
            r"\bdo\b",
            r"\bfinish\b",
            r"\bcall\b",
            r"\bmessage\b",
            r"\bremind\b",
            r"\bsend\b",
        )

        has_action = any(
            re.search(
                pattern,
                text,
            )
            for pattern in action_patterns
        )

        if not has_action:
            return None

        return {
            "intent": "task",
            "confidence": 0.90,
            "source": "semantic",
        }

    # ==========================
    # Detect
    # ==========================

    @staticmethod
    def detect(message: str):

        if not message:
            return None

        text = TaskRouter._normalize(
            message
        )

        if not text:
            return None

        result = TaskRouter._detect_explicit(
            text
        )

        if result:
            return result

        return TaskRouter._detect_semantic(
            text
        )

