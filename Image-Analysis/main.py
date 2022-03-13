import os
import sys
import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image


def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")


def main():
    subscription_key: str = None
    endpoint: str = None
    read_image_url: str = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"

    args_1: tuple = ("--subscription-key", "-skey")
    args_2: tuple = ("--endpoint", "-endp")
    args_3: tuple = ("--url", "-u")

    if args_1[0] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: endpoint = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: endpoint = sys.argv[sys.argv.index(args_2[1]) + 1]

    if args_3[0] in sys.argv: read_image_url = sys.argv[sys.argv.index(args_3[0]) + 1]
    if args_3[1] in sys.argv: read_image_url = sys.argv[sys.argv.index(args_3[1]) + 1]

    # subscription_key: str = os.environ.get("COMPUTER_VISION_SUBSCRIPTION_KEY")
    # endpoint: str = os.environ.get("COMPUTER_VISION_ENDPOINT")

    assert subscription_key is not None, "subscription_key is not set"
    assert endpoint is not None, "endpoint is not set"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Call API
    description_results = computervision_client.describe_image(read_image_url)

    # Get the captions (descriptions) from the response, with confidence level
    breaker()
    print("Description of Image \n")

    if len(description_results.captions) == 0:
        print("No description detected !!!")
    else:
        for caption in description_results.captions:
            print(f"'{caption.text.title()}' with confidence {caption.confidence * 100:.2f}")
    breaker()

if __name__ == "__main__":
    sys.exit(main() or 0)
