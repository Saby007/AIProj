from openai import AzureOpenAI
import os
import dotenv

dotenv.load_dotenv()

def main():
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version = "2024-05-01-preview"
    )

    deployment_id = "whisper"
    audio_test_file = "<Your audio file path>"
    print("Processing the audio file.....")
    result = client.audio.transcriptions.create(
        file=open(audio_test_file, "rb"),
        model=deployment_id
    )
    print(result)

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()

    