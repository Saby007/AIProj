import requests
def convert_text_to_speech(chat):
    url = f"<Your url>"
    headers = {
        "api-key": "<Your api-key>",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts",
        "input": chat,
        "voice": "alloy"
    }
    response = requests.post(url, headers=headers, json=data)
    with open("speech.mp3", "wb") as f:
        f.write(response.content)

def convert_text_to_speech_hd(chat):
    url = f"<Your url>"
    headers = {
        "api-key": "<Your api-key>",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-hd",
        "input": chat,
        "voice": "alloy"
    }
    response = requests.post(url, headers=headers, json=data)
    with open("speech_hd.mp3", "wb") as f:
        f.write(response.content)

def main():
    while True:
        print("Please enter your chat or press 'bye' to exit:")
        chat = input("User: ")
        if chat == "bye":
            break

        convert_text_to_speech(chat)
        convert_text_to_speech_hd(chat)
        print("Speech saved as speech.mp3")

main()