import requests
import os
import dotenv

def main():

    url = "" + "/speechtotext/transcriptions:transcribe?api-version=2024-11-15"
    subscription_key = ''
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    files = {
        "audio": open("C:\\Users\\ssamadda\\OneDrive - Microsoft\\Documents\\Work\\Workshops\\AOAI\\Trimble\\katiesteve.wav", "rb"),
        "definition": (None, '{"locales":["en-US"], "diarization": {"maxSpeakers": 2,"enabled": true}}', "application/json"),
    }

    response = requests.post(url, headers=headers, files=files)

    print("Status code:", response.status_code)
    if response.ok:
        data = response.json()
        combined_phrases = data.get("combinedPhrases", [])
        for phrase in combined_phrases:
            print("Combined Phrase:", phrase.get("text"))
    else:
        print("Response:", response.text)

if __name__ == "__main__":
    dotenv.load_dotenv()  
    main()
