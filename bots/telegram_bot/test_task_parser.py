from services.tasks.parser import TaskParser


tests = [

    "یادم بنداز فردا پروژه حافظه را بررسی کنم",

    "یادآوری کن امروز گزارش را ارسال کنم"

]


for item in tests:

    print(
        TaskParser.parse(item)
    )