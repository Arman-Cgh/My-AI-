from services.ai.config import AI_PROVIDER


class ProviderManager:

    def __init__(self):
        self.providers = {}

    def get_provider(self, name=None):

        provider_name = name or AI_PROVIDER

        if provider_name not in self.providers:

            if provider_name == "groq":

                from .groq_provider import GroqProvider

                self.providers[provider_name] = GroqProvider()

            else:
                raise ValueError(f"Provider '{provider_name}' not supported")

        return self.providers[provider_name]