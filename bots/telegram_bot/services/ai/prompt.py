from .config import SYSTEM_PROMPT
from .personality import Personality

import json


MAX_HISTORY_MESSAGES = 10



def build_prompt(
    user_id=None,
    user_message="",
    profile=None,
    history=None,
    memory="",
    state=None,
    current_time="",
    context=None,
    datetime=None
):


    # ==========================
    # Context compatibility
    # ==========================

    if context:

        profile = context.get(
            "profile",
            profile
        )

        history = context.get(
            "history",
            history
        )

        memory = context.get(
            "memory",
            memory
        )

        state = context.get(
            "state",
            state
        )


    if datetime:

        current_time = datetime



    # ==========================
    # Personality
    # ==========================

    personality = Personality(
        profile=profile,
        memory=memory,
        state=state
    ).build()



    # ==========================
    # Memory
    # ==========================

    if isinstance(memory, dict):

        memory_text = "\n".join(

            [

                f"- {key}: {value}"

                for key, value in memory.items()

                if value

            ]

        )


    else:

        memory_text = (

            memory

            if memory

            else

            "حافظه‌ای ثبت نشده است."

        )



    # ==========================
    # Profile
    # ==========================

    profile_text = json.dumps(

        profile or {},

        ensure_ascii=False,

        separators=(
            ",",
            ":"
        )

    )



    # ==========================
    # State
    # ==========================

    state_text = json.dumps(

        state or {},

        ensure_ascii=False,

        separators=(
            ",",
            ":"
        )

    )



    # ==========================
    # History
    # ==========================

    history = (

        history or []

    )[-MAX_HISTORY_MESSAGES:]



    history_text = "\n".join(

        [

            f"{item['role']}: {item['content']}"

            for item in history

            if item.get("content")

        ]

    )


    if not history_text:

        history_text = (
            "تاریخچه‌ای وجود ندارد."
        )



    # ==========================
    # System Prompt
    # ==========================

    system_message = f"""

{SYSTEM_PROMPT}


نام دستیار:
PF-AI


شخصیت دستیار:
{personality}


زمان فعلی:
{current_time}


اطلاعات کاربر:
{profile_text}


وضعیت کاربر:
{state_text}


حافظه بلند مدت:
{memory_text}


گفتگوهای اخیر:
{history_text}



قوانین پاسخ:

- همیشه از اطلاعات موجود استفاده کن.
- اطلاعات ذخیره شده را دوباره از کاربر نپرس.
- چیزی که نمی‌دانی را حدس نزن.
- پاسخ طبیعی و فارسی باشد.
- خودت را PF-AI معرفی کن.
- اگر اطلاعاتی برای حافظه مناسب بود، فقط از سیستم حافظه استفاده کن.


"""


    return [

        {
            "role": "system",
            "content": system_message.strip()
        },

        {
            "role": "user",
            "content": user_message
        }

    ]