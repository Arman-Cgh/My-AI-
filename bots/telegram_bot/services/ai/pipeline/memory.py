from services.ai.extractor import extract_memory
from services.ai.extraction_router import ExtractionRouter



class MemoryPipeline:


    @staticmethod
    async def process(
        provider,
        user_id: int,
        intent: str,
        user_message: str,
        response: str
    ):


        try:

            should_extract = ExtractionRouter.should_extract(
                intent,
                user_message,
                response
            )


            if not should_extract:

                print(
                    "MEMORY EXTRACTION SKIP"
                )

                return



            print(
                "MEMORY EXTRACTION RUN"
            )


            await extract_memory(
                provider,
                user_id,
                user_message,
                response
            )


        except Exception as e:

            print(
                "MEMORY PIPELINE ERROR:",
                e
            )