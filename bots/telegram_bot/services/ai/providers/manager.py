import logging

from services.ai.config import AI_PROVIDER


logger = logging.getLogger(__name__)


class ProviderManager:


    def __init__(self):

        self.providers = {}



    def get_provider(
        self,
        name=None
    ):

        provider_name = name or AI_PROVIDER


        if provider_name in self.providers:
            return self.providers[provider_name]


        provider = self._load_provider(
            provider_name
        )


        self.providers[provider_name] = provider


        return provider



    def _load_provider(
        self,
        provider_name
    ):


        if provider_name == "groq":

            from .groq_provider import GroqProvider

            return GroqProvider()



        if provider_name == "openrouter":

            from .openrouter_provider import OpenRouterProvider

            return OpenRouterProvider()



        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )



    async def generate(
        self,
        messages,
        intent=None
    ):

        primary_name = AI_PROVIDER


        provider = self.get_provider(
            primary_name
        )


        try:

            response = await provider.generate(
                messages
            )


            return {

                "text": response,

                "provider": primary_name

            }



        except Exception as e:


            logger.warning(
                f"{primary_name} failed: {e}"
            )


            fallback = self.get_fallback_provider(
                primary_name
            )


            response = await fallback.generate(
                messages
            )


            return {

                "text": response,

                "provider": self.get_provider_name(
                    fallback
                )

            }



    def get_fallback_provider(
        self,
        failed_provider
    ):


        if failed_provider == "groq":

            return self.get_provider(
                "openrouter"
            )


        return self.get_provider(
            "groq"
        )



    def get_provider_name(
        self,
        provider
    ):


        name = provider.__class__.__name__


        if name == "GroqProvider":
            return "groq"


        if name == "OpenRouterProvider":
            return "openrouter"


        return "unknown"