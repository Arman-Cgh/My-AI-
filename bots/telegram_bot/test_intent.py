from services.ai.intent_router import IntentRouter



tests = [

    "یادم بنداز فردا پروژه رو بررسی کنم",

    "اسم من چیه؟",

    "یه کد پایتون بنویس",

    "سلام خوبی؟"

]


for text in tests:

    result = IntentRouter.detect(text)

    print(
        text,
        "=>",
        result
    )