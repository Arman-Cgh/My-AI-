import json
import re

from services.ai.model_router import ModelRouter
from services.ai.logger import AILogger


class InformationExtractor:

    def __init__(
        self,
        config=None
    ):
        self.config = config

    async def extract(
        self,
        user_id: int,
        user_message: str,
        assistant_response: str = "",
        provider=None,
        provider_name=None,
    ):

        if provider is None:
            return {}

        return await extract_memory(
            provider=provider,
            provider_name=provider_name,
            user_id=user_id,
            user_message=user_message,
            assistant_response=assistant_response
        )


def _clean_memory(
    memory: dict
):

    if not isinstance(memory, dict):
        return {}

    allowed = {
        "name",
        "job",
        "interests",
        "location",
        "preferences"
    }

    cleaned = {}

    for key, value in memory.items():

        key = str(
            key
        ).strip().lower()

        if key not in allowed:
            continue

        if value is None:
            continue

        if isinstance(value, list):
            value = ", ".join(
                map(
                    str,
                    value
                )
            )

        value = str(
            value
        ).strip()

        if not value:
            continue

        if len(value) > 100:
            continue

        cleaned[key] = value

    return cleaned


def _clean_state(
    state: dict
):

    if not isinstance(state, dict):
        return {}

    return {
        key: value
        for key, value in state.items()
        if value is not None
    }


async def extract_memory(
    provider,
    provider_name,
    user_id: int,
    user_message: str,
    assistant_response: str,
):

    prompt = f"""
Extract only permanent useful user information.

Return ONLY JSON.

Format:

{{
"memory": {{}},
"state": {{}}
}}

Rules:

- Do not save temporary requests.
- Do not save conversation content.
- Save only permanent user facts.

Allowed memory:

name
job
interests
location
preferences

User:

{user_message}

Assistant:

{assistant_response}
"""

    try:

        model = ModelRouter.select(
            provider_name,
            "memory"
        )

        response = await provider.generate(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model
        )

        if isinstance(
            response,
            dict
        ):
            response = response.get(
                "text",
                ""
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

        return {
            "memory": _clean_memory(
                data.get(
                    "memory",
                    {}
                )
            ),
            "state": _clean_state(
                data.get(
                    "state",
                    {}
                )
            )
        }

    except Exception as e:

        AILogger.error(
            f"Extractor error: {e}"
        )

        return {}