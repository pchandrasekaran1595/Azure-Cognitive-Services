import os
import sys

import azure.cognitiveservices.speech as speechsdk

READ_PATH = "Files"


def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")



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



if __name__ == "__main__":
    sys.exit(main() or 0)
