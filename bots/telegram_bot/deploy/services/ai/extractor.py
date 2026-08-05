import json
import re

from services.ai.providers.manager import ProviderManager
from services.ai.router import select_model
from services.ai.memory_manager import MemoryManager


provider = ProviderManager().get_provider()


async def extract_memory(
    user_id: int,
    user_message: str,
    assistant_response: str
):

    prompt = f"""
Extract useful user information.

Return ONLY JSON.
No markdown.
No explanation.

Format:

{{
"name":"",
"job":"",
"interests":"",
"projects":"",
"preferences":""
}}

User message:
{user_message}

Assistant response:
{assistant_response}
"""


    try:

        response = await provider.generate(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            select_model("memory")
        )


        cleaned = response.strip()

        cleaned = re.sub(
            r"```json|```",
            "",
            cleaned
        ).strip()


        match = re.search(
            r"\{.*\}",
            cleaned,
            re.DOTALL
        )


        if not match:
            print(
                "Extractor invalid:",
                response
            )
            return {}


        data = json.loads(
            match.group()
        )


        if data:

            MemoryManager.update(
                user_id,
                data
            )


        return data


    except Exception as e:

        print(
            "Extractor Error:",
            e
        )

        return {}