import json
import re

from services.ai.memory_manager import MemoryManager
from services.ai.state_manager import StateManager
from services.ai.router import select_model

from services.ai.logger import AILogger




async def extract_memory(

    provider,

    user_id:int,

    user_message:str,

    assistant_response:str

):


    prompt = f"""

Extract useful user information.

Return ONLY JSON.

Format:

{{
"memory":{{}},
"state":{{}}
}}


User:
{user_message}


Assistant:
{assistant_response}

"""


    try:


        response = await provider.generate(

            [
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            select_model("memory")

        )



        cleaned = re.sub(

            r"```json|```",

            "",

            response

        ).strip()



        match = re.search(

            r"\{.*\}",

            cleaned,

            re.DOTALL

        )


        if not match:

            AILogger.warning(
                "Invalid extractor JSON"
            )

            return {}



        data = json.loads(
            match.group()
        )



        memory = data.get(
            "memory",
            {}
        )


        state = data.get(
            "state",
            {}
        )



        if memory:

            MemoryManager.update(

                user_id,

                memory

            )



        if state:

            StateManager.update(

                user_id,

                state

            )



        return data



    except Exception as e:


        AILogger.error(
            f"Extractor error: {e}"
        )


        return {}