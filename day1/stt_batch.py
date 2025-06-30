import requests
import os
import time
import dotenv

def start_transcription(speech_endpoint, speech_key, payload):
    url = f"{speech_endpoint}/speechtotext/v3.2/transcriptions"
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    transcription = response.json()
    transcription_id = transcription["self"].split("/")[-1]
    print(f"Transcription started. ID: {transcription_id}")
    return transcription_id

def poll_status(speech_endpoint, speech_key, transcription_id):
    status_url = f"{speech_endpoint}/speechtotext/v3.2/transcriptions/{transcription_id}"
    headers = {"Ocp-Apim-Subscription-Key": speech_key}
    while True:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        status = response.json()
        print(f"Status: {status['status']}")
        if status["status"] in ["Succeeded", "Failed"]:
            return status["status"]
        time.sleep(5)

def get_results(speech_endpoint, speech_key, transcription_id):
    files_url = f"{speech_endpoint}/speechtotext/v3.2/transcriptions/{transcription_id}/files"
    headers = {"Ocp-Apim-Subscription-Key": speech_key}
    response = requests.get(files_url, headers=headers)
    response.raise_for_status()
    files = response.json()
    print("Result files info:")
    for file in files.get("values", []):
        print(f"{file['kind']}: {file['links']['contentUrl']}")

def main():
    speech_key = "<your_speech_key>"
    speech_endpoint = "<your_speech_endpoint>"  # e.g., "https://eastus.api.cognitive.microsoft.com"
    payload = {
        "contentUrls": [
            "https://crbn.us/hello.wav",
            "https://crbn.us/whatstheweatherlike.wav"
        ],  
        "locale": "en-US",
        "displayName": "My Transcription",
        "properties": {
            "wordLevelTimestampsEnabled": True,
            "languageIdentification": {
                "candidateLocales": [
                    "en-US", "de-DE", "es-ES"
                ]
            }
        }
    }
    transcription_id = start_transcription(speech_endpoint, speech_key, payload)
    status = poll_status(speech_endpoint, speech_key, transcription_id)
    if status == "Succeeded":
        get_results(speech_endpoint, speech_key, transcription_id)
    else:
        print("Transcription failed.")

if __name__ == "__main__":
    dotenv.load_dotenv()  # Load environment variables from .env file
    main()