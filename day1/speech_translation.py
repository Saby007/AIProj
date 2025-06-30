import os
import azure.cognitiveservices.speech as speechsdk
import dotenv

def recognize_from_microphone():
    # This example requires environment variables named "API_KEY" and "REGION"
    speech_key = os.environ.get("API_KEY")
    speech_region = os.environ.get("REGION")
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=speech_region)
    speech_translation_config.speech_recognition_language="en-US"

    to_language ="ta"
    speech_translation_config.add_target_language(to_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    #audio_config = speechsdk.audio.AudioConfig(filename="file.wav")
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("Speak into your microphone.")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_language = "ta-IN"

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(translation_recognition_result.text))
        print("""Translated into '{}': {}""".format(
            to_language, 
            translation_recognition_result.translations[to_language]))
        synthesizer.speak_text_async(translation_recognition_result.translations[to_language]).get()
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

def main():
    recognize_from_microphone()

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()