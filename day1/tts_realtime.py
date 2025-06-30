import os
import azure.cognitiveservices.speech as speechsdk
import dotenv
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"



def main():
    speech_key = os.environ.get('API_KEY')
    region = os.environ.get('REGION')

    if not speech_key or not region:
        raise ValueError("Please set the API_KEY and REGION environment variables.")

    print("Welcome to the Real-Time Text-to-Speech Demo!")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    
    # The neural multilingual voice can speak different languages based on the input text.
    speech_config.speech_synthesis_language = "en-US" 
    speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    #Stream
    #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)


    # Get text from the console and synthesize to the default speaker.
    print("Enter some text that you want to speak >")
    text = input()

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    #Stream
    #speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    #stream = speechsdk.AudioDataStream(speech_synthesis_result)
    #stream.save_to_wav_file("file.wav")

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()