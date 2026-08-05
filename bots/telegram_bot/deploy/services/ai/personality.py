class Personality:


    def __init__(
        self,
        profile: dict = None,
        memory=None,
        state: dict = None
    ):

        self.profile = profile or {}
        self.memory = self.format_memory(memory)
        self.state = state or {}

    def format_memory(self, memory):
        if isinstance(memory, dict):
            lines = [f"- {key}: {value}" for key, value in memory.items() if value is not None]
            return "\n".join(lines)

        return str(memory or "")



    def build(self):


        name = self.profile.get(
            "first_name",
            ""
        )


        if not name:

            name = self.extract_memory(
                "name"
            )



        job = self.extract_memory(
            "job"
        )


        interests = self.extract_memory(
            "interests"
        )



        text = f"""

شخصیت AetherAI:

نام کاربر:
{name}


شغل کاربر:
{job}


علایق کاربر:
{interests}


قوانین رفتار:

- تو AetherAI هستی، دستیار هوشمند شخصی کاربر.
- دوستانه و طبیعی صحبت کن.
- اگر نام کاربر را می‌دانی گاهی استفاده کن.
- اطلاعات حافظه را در پاسخ‌ها استفاده کن.
- خودت را مدل عمومی هوش مصنوعی معرفی نکن.
- پاسخ‌ها را واضح و کاربردی بده.
- برای مسائل فنی توضیح مرحله‌ای بده.
- برای سوال‌های ساده کوتاه جواب بده.

"""


        return text.strip()



    def extract_memory(
        self,
        key
    ):

        for line in self.memory.split("\n"):

            if key in line:

                return (
                    line
                    .replace(
                        "-",
                        ""
                    )
                    .replace(
                        key + ":",
                        ""
                    )
                    .strip()
                )


        return ""