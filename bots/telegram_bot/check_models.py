from openai import OpenAI
from services.ai.config import AI_API_KEY, AI_BASE_URL


client = OpenAI(
    api_key=AI_API_KEY,
    base_url=AI_BASE_URL
)


models = client.models.list()


for m in models.data:
    if ":free" in m.id:
        print(m.id)