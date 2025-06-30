import os
import azure.cognitiveservices.speech as speechsdk
import dotenv

def recognize_from_microphone():
    # This example requires environment variables "API_KEY" and "REGION"
    speech_key = os.environ.get('API_KEY')
    region = os.environ.get('REGION')

    if not speech_key or not region:
        raise ValueError("Please set the API_KEY and REGION environment variables.")
    # Get AAD token using managed identity
    #token = get_speech_token(endpoint)      

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    GREEN = "\033[92m"
    RESET = "\033[0m"

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"{GREEN}Recognized: {speech_recognition_result.text}{RESET}")
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(f"{GREEN}No speech could be recognized: {speech_recognition_result.no_match_details}{RESET}")
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print(f"{GREEN}Speech Recognition canceled: {cancellation_details.reason}{RESET}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"{GREEN}Error details: {cancellation_details.error_details}{RESET}")
            print("Did you set the speech resource key and endpoint values?")

def main():
    print("Welcome to the Real-Time from Microphone Speech-to-Text Demo!")
    recognize_from_microphone()

dotenv.load_dotenv()  
main()