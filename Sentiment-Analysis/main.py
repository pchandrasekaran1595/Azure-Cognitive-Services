import os
import sys

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

READ_PATH = "Files"


def authenticate_client(key: str, endpoint: str):
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client


def analyze_sentiment(client, documents: list):
    response = client.analyze_sentiment(documents=documents)[0]

    response = client.analyze_sentiment(documents=documents)[0]
    breaker()
    print(f"Document Sentiment: {response.sentiment.title()}")
    print(f"Overall scores: Positive={response.confidence_scores.positive:.2f}; Neutral={response.confidence_scores.neutral:.2f}; Negative={response.confidence_scores.negative:.2f} \n")
    for idx, sentence in enumerate(response.sentences):
        print(f"Sentence: {sentence.text}")
        print(f"Sentence {idx+1} sentiment: {sentence.sentiment}")
        print(f"Sentence score: Positive={sentence.confidence_scores.positive:.2f}; Neutral={sentence.confidence_scores.neutral:.2f}; Negative={sentence.confidence_scores.negative:.2f}\n")
    breaker()

def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")


def main():
    subscription_key: str = None
    endpoint: str = None
    filename: str = "Test.txt"
    documents: list = []

    args_1: tuple = ("--subscription-key", "-skey")
    args_2: tuple = ("--endpoint", "-endp")
    args_3: tuple = ("--file", "-f")

    if args_1[0] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: subscription_key = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: endpoint = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: endpoint = sys.argv[sys.argv.index(args_2[1]) + 1]

    if args_3[0] in sys.argv: filename = sys.argv[sys.argv.index(args_3[0]) + 1]
    if args_3[1] in sys.argv: filename = sys.argv[sys.argv.index(args_3[1]) + 1]

    # subscription_key: str = os.environ.get("LANGUAGE_SUBSCRIPTION_KEY")
    # endpoint: str = os.environ.get("LANGUAGE_ENDPOINT")

    assert subscription_key is not None, "subscription_key is not set"
    assert endpoint is not None, "endpoint is not set"

    named_entities_extractor_client = authenticate_client(subscription_key, endpoint)

    with open(os.path.join(READ_PATH, filename), "r") as f: text = f.read()
    documents.append(text)

    analyze_sentiment(named_entities_extractor_client, documents)


if __name__ == "__main__":
    sys.exit(main() or 0)
