from services.ai.intents import IntentResult



class IntentRouter:



    RULES = {


        "task": {

            "keywords": [

                "یادم بنداز",

                "یادآوری",

                "یادآوری کن",

                "یک کار",

                "وظیفه",

                "task",

                "remind"

            ],

            "confidence": 0.95

        },



        "memory": {

            "keywords": [

                "اسم من",

                "من کی هستم",

                "درباره من",

                "یادت باشه",

                "به خاطر بسپار"

            ],

            "confidence": 0.90

        },



        "code": {

            "keywords": [

                "کد",

                "python",

                "پایتون",

                "برنامه نویسی",

                "خطا",

                "error"

            ],

            "confidence": 0.85

        }


    }



    @staticmethod
    def detect(
        message: str
    ):


        if not message:

            return IntentResult(
                "chat",
                0.0,
                "empty"
            )



        text = message.lower().strip()



        best_match = None



        best_score = 0



        for intent, data in IntentRouter.RULES.items():


            for keyword in data["keywords"]:


                if keyword.lower() in text:


                    score = data["confidence"]



                    if score > best_score:

                        best_score = score

                        best_match = intent



        if best_match:


            return IntentResult(

                best_match,

                best_score,

                "keyword"

            )



        return IntentResult(

            "chat",

            0.5,

            "default"

        )