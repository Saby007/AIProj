# os.getenv() for the endpoint and key assumes that you are using environment variables.

import os
import dotenv

dotenv.load_dotenv()
from openai import AzureOpenAI
client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-12-01-preview"
    )

chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps people find information."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tell me a joke on Saby "
                    }
                ]
            }
        ]

response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=chat_prompt
    # Content that is detected at severity level medium or high is filtered, 
    # while content detected at severity level low isn't filtered by the content filters.
)

print(response.model_dump_json(indent=2))