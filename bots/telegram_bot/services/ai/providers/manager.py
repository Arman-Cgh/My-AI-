from services.ai.config import AI_PROVIDER


class ProviderManager:


    def __init__(self):

        self.providers = {}



    def get_provider(self, name=None):

        provider_name = name or AI_PROVIDER


        if provider_name in self.providers:

            return self.providers[provider_name]



        provider = self._load_provider(provider_name)


        self.providers[provider_name] = provider


        return provider




    def _load_provider(self, provider_name):


        if provider_name == "groq":

            from .groq_provider import GroqProvider

            return GroqProvider()



        raise ValueError(
            f"Provider '{provider_name}' not supported"
        )