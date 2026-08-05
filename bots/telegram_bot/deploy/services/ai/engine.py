from services.ai.context import ContextBuilder
from services.ai.prompt import build_prompt
from services.ai.router import select_model

from services.ai.providers.manager import ProviderManager

from services.ai.extractor import extract_memory


class AIEngine:


    def __init__(self):

        self.provider_manager = ProviderManager()



    async def ask(
        self,
        user_id: int,
        user_message: str
    ):

        try:

            # ==========================
            # Context
            # ==========================

            context = ContextBuilder(
                user_id
            ).build()


            print(
                "===== CONTEXT ====="
            )

            print(
                context
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
            # Model
            # ==========================

            model = select_model(
                "chat"
            )


            print(
                "SELECTED MODEL:",
                model
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
            # Memory
            # ==========================

            try:

                await extract_memory(

                    user_id,

                    user_message,

                    response

                )

            except Exception as e:

                print(
                    "Extractor Error:",
                    e
                )


            return response



        except Exception as e:

            print(
                "ENGINE ERROR:",
                e
            )


            return (
                "متاسفانه مشکلی در پردازش درخواست پیش آمد. "
                "لطفاً بعداً دوباره تلاش کنید."
            )