from services.ai.context import ContextBuilder
from services.ai.prompt import build_prompt
from services.ai.router import select_model

from services.ai.providers.manager import ProviderManager

from services.ai.extractor import extract_memory
from services.ai.intent_router import IntentRouter
from services.ai.cache import AICache
from services.ai.extraction_router import ExtractionRouter

from services.tasks.parser import TaskParser
from services.tasks.manager import TaskManager



class AIEngine:


    def __init__(self):

        self.provider_manager = ProviderManager()

        self.cache = AICache()



    async def ask(
        self,
        user_id: int,
        user_message: str
    ):

        try:


            # ==========================
            # Intent Detection
            # ==========================

            intent_result = IntentRouter.detect(
                user_message
            )


            print(
                "INTENT:",
                intent_result
            )


            # سازگاری با IntentResult جدید

            if hasattr(
                intent_result,
                "intent"
            ):

                intent = intent_result.intent


            elif isinstance(
                intent_result,
                dict
            ):

                intent = intent_result.get(
                    "intent",
                    "chat"
                )


            else:

                intent = intent_result



            # ==========================
            # Task Handler
            # ==========================

            if intent == "task":


                task_data = TaskParser.parse(
                    user_message
                )


                task_id = TaskManager.create(

                    user_id,

                    task_data["title"],

                    description="",

                    due_date=task_data["due_date"] or ""

                )


                return (

                    f"✅ کار ثبت شد\n\n"

                    f"📝 {task_data['title']}\n"

                    f"📅 {task_data['due_date'] or 'بدون تاریخ'}\n"

                    f"🆔 شناسه: {task_id}"

                )



            # ==========================
            # Model Selection
            # ==========================


            model = select_model(
                intent
            )


            print(
                "MODEL:",
                model
            )



            # ==========================
            # Cache
            # ==========================


            cacheable = self.cache.is_cacheable(

                intent,

                user_message

            )


            cache_key = None



            if cacheable:


                cache_key = self.cache.generate_key(

                    user_message,

                    intent,

                    model

                )


                cached_answer = self.cache.get(

                    user_id,

                    cache_key

                )


                if cached_answer:


                    print(
                        "CACHE HIT"
                    )


                    return cached_answer



            else:


                print(
                    "CACHE BYPASS"
                )



            # ==========================
            # Context
            # ==========================


            context = ContextBuilder(

                user_id

            ).build(

                intent

            )


            print(
                "CONTEXT READY"
            )



            # ==========================
            # Prompt
            # ==========================


            messages = build_prompt(

                profile=context["profile"],

                memory=context["memory"],

                history=context["history"],

                state=context["state"],

                current_time=context["datetime"],

                user_message=user_message

            )



            # ==========================
            # Provider
            # ==========================


            provider = self.provider_manager.get_provider()



            response = await provider.generate(

                messages,

                model

            )



            # ==========================
            # Save Cache
            # ==========================


            if cacheable and cache_key:


                self.cache.set(

                    user_id,

                    cache_key,

                    response

                )



            # ==========================
            # Memory Extraction
            # ==========================


            try:


                if ExtractionRouter.should_extract(

                    intent,

                    user_message,

                    response

                ):


                    print(
                        "MEMORY EXTRACTION RUN"
                    )


                    await extract_memory(

                        provider,

                        user_id,

                        user_message,

                        response

                    )


                else:


                    print(
                        "MEMORY EXTRACTION SKIP"
                    )


            except Exception as e:


                print(

                    "EXTRACTOR ERROR:",

                    e

                )



            return response



        except Exception as e:


            print(

                "ENGINE ERROR:",

                e

            )


            return (

                "متاسفانه در پردازش درخواست مشکلی پیش آمد."

            )