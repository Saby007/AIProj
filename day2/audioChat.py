import base64
import os
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()

# Set environment variables or edit the corresponding values here.
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(
    api_version="2025-01-01-preview",  
    api_key=api_key, 
    azure_endpoint=endpoint
)

# Read and encode audio file  
with open('dog.wav', 'rb') as wav_reader: 
    encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 

# Make the audio chat completions request
completion = client.chat.completions.create( 
    model="gpt-4o-audio-preview", 
    modalities=["text", "audio"], 
    audio={"voice": "alloy", "format": "wav"}, 
    messages=[ 
        { 
            "role": "user", 
            "content": [ 
                {  
                    "type": "text", 
                    "text": "which dog is good for family?" 
                }, 
                { 
                    "type": "input_audio", 
                    "input_audio": { 
                        "data": encoded_string, 
                        "format": "wav" 
                    } 
                } 
            ] 
        }, 
    ] 
) 

print(completion.choices[0].message.audio.transcript)

# Write the output audio data to a file
wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
with open("analysis.wav", "wb") as f:
    f.write(wav_bytes)