import os
import sys
import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image


READ_PATH = "Files"


def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")


def main():
    subscription_key: str = None
    endpoint: str = None
    # read_image_url: str = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"
    read_image_url: str = None
    filename: str = "Test.png"

    args_1: tuple = ("--subscription-key", "-skey")
    args_2: tuple = ("--endpoint", "-endp")
    args_3: tuple = ("--url", "-u")
    args_4: tuple = ("--file", "-f")

    if args_1[0] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: endpoint = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: endpoint = sys.argv[sys.argv.index(args_2[1]) + 1]

    if args_3[0] in sys.argv: read_image_url = sys.argv[sys.argv.index(args_3[0]) + 1]
    if args_3[1] in sys.argv: read_image_url = sys.argv[sys.argv.index(args_3[1]) + 1]

    if args_4[0] in sys.argv: filename = sys.argv[sys.argv.index(args_4[0]) + 1]
    if args_4[1] in sys.argv: filename = sys.argv[sys.argv.index(args_4[1]) + 1]

    # subscription_key: str = os.environ.get("COMPUTER_VISION_SUBSCRIPTION_KEY")
    # endpoint: str = os.environ.get("COMPUTER_VISION_ENDPOINT")

    assert subscription_key is not None, "subscription_key is not set"
    assert endpoint is not None, "endpoint is not set"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    # Call API with URL and raw response (allows you to get the operation location)
    if read_image_url is not None:
        read_response = computervision_client.read(read_image_url, raw=True)
        # read_response = computervision_client.read(read_image_url, raw=True, model_version="2022-01-30-preview")
    else:
        read_response = computervision_client.read_in_stream(open(os.path.join(READ_PATH, filename), "rb"), raw=True)
        # read_response = computervision_client.read_in_stream(open(os.path.join(READ_PATH, filename), "rb"), raw=True, model_version="2022-01-30-preview")


    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]


    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)


    # Print the detected text, line by line
    breaker()
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)
    breaker()


if __name__ == "__main__":
    sys.exit(main() or 0)
