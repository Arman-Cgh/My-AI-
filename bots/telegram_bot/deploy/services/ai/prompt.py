from .config import SYSTEM_PROMPT
from .personality import Personality
import json


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

    # compatibility layer
    if context:

        profile = context.get("profile", profile)

        history = context.get("history", history)

        memory = context.get("memory", memory)

        state = context.get("state", state)

    if datetime:
        current_time = datetime


    personality = Personality(
        profile=profile,
        memory=memory,
        state=state
    ).build()


    if isinstance(memory, dict):

        memory_text = "\n".join(
            [
                f"- {k}: {v}"
                for k,v in memory.items()
                if v
            ]
        )

    else:
        memory_text = memory or "حافظه‌ای ثبت نشده است."


    profile_text = json.dumps(
        profile or {},
        ensure_ascii=False,
        indent=2
    )


    state_text = json.dumps(
        state or {},
        ensure_ascii=False,
        indent=2
    )


    history_text = "\n\n".join(
        [
            f"{x['role']}: {x['content']}"
            for x in (history or [])
        ]
    )


    system_message = f"""
{SYSTEM_PROMPT}


هویت:
{personality}


زمان:
{current_time}


پروفایل کاربر:
{profile_text}


وضعیت:
{state_text}


حافظه:
{memory_text}


تاریخچه:
{history_text}


قوانین:
- از اطلاعات حافظه استفاده کن.
- اگر اطلاعات داری دوباره سوال نپرس.
- پاسخ طبیعی و دوستانه بده.
"""


    return [

        {
            "role":"system",
            "content":system_message
        },

        {
            "role":"user",
            "content":user_message
        }

    ]