from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="This is a fine day"
)

print(response.model_dump_json(indent=2))
