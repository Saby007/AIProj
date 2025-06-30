import os
from openai import AzureOpenAI
import time
import dotenv

dotenv.load_dotenv()
    
client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-12-01-preview"
    )

# Upload a file with a purpose of "batch"
file = client.files.create(
  file=open("image_url.jsonl", "rb"), 
  purpose="batch"
)

time.sleep(60)
print(file.model_dump_json(indent=2))

file_id = file.id

# Submit a batch job with the file
batch_response = client.batches.create(
    input_file_id=file_id,
    endpoint="/chat/completions",
    completion_window="24h",
)

# Save batch ID for later use
batch_id = batch_response.id

print(batch_response.model_dump_json(indent=2))