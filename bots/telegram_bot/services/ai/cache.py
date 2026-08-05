import hashlib

from database.db import get_cached_answer, save_cached_answer


class AICache:

    PROMPT_VERSION = "1"

    BYPASS_INTENTS = ("task", "memory")

    CHAT_BYPASS_PATTERNS = [
        "continue",
        "continue please",
        "explain more",
        "another example",
        "why",
        "what do you mean",
        "what did we discuss",
        "what did we talk about",
        "summarize",
        "my name",
        "what is my name",
        "what am i working on",
        "what am i doing",
        "do you remember",
        "what do you remember",
        "remember",
        "save this",
        "yesterday",
        "today",
        "now",
        "current time",
        "current date",
        "profile",
        "memory",
        "history",
        "state",
        "task",
        "my project",
        "current project",
        "current goal",
        "my goal",
        "what are my goals",
        "what is my goal",
        "what is my project",
        "what project am i",
        "what am i",
        "how am i",
        "what should i",
        "should i",
        "یادم بنداز",
        "یادآوری",
        "یادآوری کن",
        "یک کار",
        "وظیفه",
        "اسم من",
        "من کی هستم",
        "درباره من",
        "یادت باشه",
        "به خاطر بسپار",
        "ادامه",
        "بیشتر توضیح بده",
        "یک مثال دیگر",
        "چرا",
        "چه منظوری داری",
        "چه چیزی رو گفتم",
        "دیروز",
        "امروز",
        "حالا",
        "فعلا",
        "آیا یادت میاد",
        "خاطره",
        "تاریخچه",
        "پروژه من",
        "هدف من",
    ]

    def __init__(self, prompt_version=None):
        self.prompt_version = prompt_version or self.PROMPT_VERSION

    def _normalize_text(self, text):
        return " ".join(str(text or "").strip().lower().split())

    def generate_key(
        self,
        user_message,
        intent,
        model,
        prompt_version=None
    ):
        normalized_message = self._normalize_text(user_message)
        version = prompt_version or self.prompt_version
        key_text = f"{version}|{intent}|{model}|{normalized_message}"
        return hashlib.sha256(key_text.encode("utf-8")).hexdigest()

    def is_cacheable(
        self,
        intent,
        user_message
    ):
        normalized_message = self._normalize_text(user_message)
        if not normalized_message:
            print("CACHE BYPASS: empty message")
            return False

        if intent in self.BYPASS_INTENTS:
            print(f"CACHE BYPASS: intent={intent} reason=explicit bypass intent")
            return False

        if intent == "code":
            return True

        if intent != "chat":
            print(f"CACHE BYPASS: intent={intent} reason=unknown non-chat/code intent")
            return False

        for pattern in self.CHAT_BYPASS_PATTERNS:
            if pattern in normalized_message:
                print(f"CACHE BYPASS: intent={intent} reason=matched bypass pattern '{pattern}'")
                return False

        return True

    def get(self, user_id, cache_key):
        return get_cached_answer(user_id, cache_key)

    def set(self, user_id, cache_key, value, ttl=None):
        # TTL is not supported by the existing SQLite schema.
        save_cached_answer(user_id, cache_key, value)
