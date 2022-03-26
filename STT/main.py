import os
import sys

import azure.cognitiveservices.speech as speechsdk

READ_PATH = "Files"


def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")


def recognize_from_microphone(speech_config: speechsdk.SpeechConfig = None, filename: str = None) -> None:
    speech_config.speech_recognition_language="en-US"

    #To recognize speech from an audio file, use `filename` instead of `use_default_microphone`:
    audio_config = speechsdk.audio.AudioConfig(filename=filename)
    # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {speech_recognition_result.text}")
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(f"No speech could be recognized: {speech_recognition_result.no_match_details}")
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")


def main():
    subscription_key: str = None
    region: str = None
    filename: str = "Test.wav"

    args_1: tuple = ("--subscription-key", "-skey")
    args_2: tuple = ("--region", "-r")
    args_3: tuple = ("--file", "-f")

    if args_1[0] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: region = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: region = sys.argv[sys.argv.index(args_2[1]) + 1]

    if args_3[0] in sys.argv: filename = sys.argv[sys.argv.index(args_3[0]) + 1]
    if args_3[1] in sys.argv: filename = sys.argv[sys.argv.index(args_3[1]) + 1]

    # subscription_key: str = os.environ.get("SPEECH_SUBSCRIPTION_KEY")
    # region: str = os.environ.get("SPEECH_REGION")

    assert subscription_key is not None, "subscription_key is not set"
    assert region is not None, "endpoint is not set"

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region="YourServiceRegion")

    recognize_from_microphone(speech_config=speech_config, filename=os.path.join(READ_PATH, filename))


if __name__ == "__main__":
    sys.exit(main() or 0)
