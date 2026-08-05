class ResponsePipeline:


    def __init__(
        self,
        provider_manager,
        cache
    ):

        self.provider_manager = provider_manager

        self.cache = cache



    async def generate(
        self,
        user_id: int,
        messages: list,
        model: str,
        intent: str,
        user_message: str
    ):


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


            cached = self.cache.get(
                user_id,
                cache_key
            )


            if cached is not None:

                print(
                    "CACHE HIT"
                )

                return (
                    cached,
                    None
                )


            print(
                "CACHE MISS"
            )


        else:

            print(
                "CACHE BYPASS"
            )



        provider = self.provider_manager.get_provider()



        response = await provider.generate(
            messages,
            model
        )



        if cacheable and cache_key:


            self.cache.set(
                user_id,
                cache_key,
                response
            )



        return (
            response,
            provider
        )