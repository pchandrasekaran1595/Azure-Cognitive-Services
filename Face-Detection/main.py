import os
import io
import sys
import glob
import time
import uuid
import asyncio
import requests

from io import BytesIO
from urllib.parse import urlparse
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition


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

    # subscription_key: str = os.environ.get("FACE_API_SUBSCRIPTION_KEY")
    # endpoint: str = os.environ.get("FACE_API_ENDPOINT")

    assert subscription_key is not None, "subscription_key is not set"
    assert endpoint is not None, "endpoint is not set"

    # Create an authenticated FaceClient.
    face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # The URL of a JPEG image to detect a single face
    detected_faces = face_client.face.detect_with_url(read_image_url)

    
if __name__ == "__main__":
    sys.exit(main() or 0)
