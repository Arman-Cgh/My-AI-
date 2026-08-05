import re

from datetime import datetime, timedelta



class TaskParser:


    REMOVE_WORDS = [

        "یادم بنداز",

        "یادآوری کن",

        "یادآوری",

        "remind me",

        "remind",

    ]


    @staticmethod
    def parse(message: str):

        text = (
            message
            .strip()
        )


        title = text



        # ==========================
        # Remove command words
        # ==========================

        for word in TaskParser.REMOVE_WORDS:

            title = title.replace(
                word,
                ""
            )



        due_date = ""



        # ==========================
        # Date detection
        # ==========================


        if "پس فردا" in text:

            due_date = (

                datetime.now()

                +

                timedelta(days=2)

            ).strftime(
                "%Y-%m-%d"
            )


            title = title.replace(
                "پس فردا",
                ""
            )



        elif "فردا" in text:

            due_date = (

                datetime.now()

                +

                timedelta(days=1)

            ).strftime(
                "%Y-%m-%d"
            )


            title = title.replace(
                "فردا",
                ""
            )



        elif "امروز" in text:

            due_date = datetime.now().strftime(
                "%Y-%m-%d"
            )


            title = title.replace(
                "امروز",
                ""
            )



        # ==========================
        # Clean title
        # ==========================

        title = re.sub(
            r"\s+",
            " ",
            title
        ).strip()



        if not title:

            title = "کار بدون عنوان"



        return {

            "title": title,

            "due_date": due_date

        }