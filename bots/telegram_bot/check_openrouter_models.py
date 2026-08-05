from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

models = client.models.list()

for model in models.data:
    if ":free" in model.id:
        print(model.id)