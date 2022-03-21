import os
import io
import sys
import cv2
import glob
import time
import uuid
import asyncio
import requests
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from urllib.parse import urlparse
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition


READ_PATH = "Files"

####################################################################################################

def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")

####################################################################################################

def getRectangle(faceDictionary: dict) -> tuple:
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))


def drawFaceRectangles(detected_faces: list, read_image_url: str=None, filename: str=None) -> None:
    if read_image_url is not None:
        response = requests.get(read_image_url)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(open(os.path.join(READ_PATH, filename), "rb"))

    # For each face returned use the face rectangle and draw a red box.
    print("\nDrawing rectangle around face... see popup for results.")
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline="red")
    return img

####################################################################################################

def show(image: np.ndarray, cmap: str="gnuplot2") -> None:
    plt.figure()
    plt.imshow(image, cmap=cmap)
    plt.axis("off")
    plt.show()

####################################################################################################

def main():
    subscription_key: str = None
    endpoint: str = None
    # read_image_url: str = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
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

    # subscription_key: str = os.environ.get("FACE_API_SUBSCRIPTION_KEY")
    # endpoint: str = os.environ.get("FACE_API_ENDPOINT")

    assert subscription_key is not None, "subscription_key is not set"
    assert endpoint is not None, "endpoint is not set"

    # Create an authenticated FaceClient.
    face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # The URL of a JPEG image to detect a single face
    if read_image_url is not None:
        detected_faces = face_client.face.detect_with_url(read_image_url)
        if not detected_faces:
            raise Exception(f"No face detected from image {read_image_url}")

        # # Display the detected face ID in the first single-face image.
        # # Face IDs are used for comparison to faces (their IDs) detected in other images.
        # print(f"Detected face ID from {read_image_url} :")
        # for face in detected_faces: print (face.face_id)
        # print()
        # # Save this ID for use in Find Similar
        # first_image_face_ID = detected_faces[0].face_id

        image = drawFaceRectangles(detected_faces, read_image_url=read_image_url)

    else:
        detected_faces = face_client.face.detect_with_stream(open(os.path.join(READ_PATH, filename), "rb"))
        if not detected_faces:
            raise Exception(f"No face detected from image {filename}")

        image = drawFaceRectangles(detected_faces, filename=filename)

    image.show()

####################################################################################################
 
if __name__ == "__main__":
    sys.exit(main() or 0)

####################################################################################################
