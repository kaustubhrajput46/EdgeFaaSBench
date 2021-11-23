import sys
import json
import nltk
nltk.download('punkt')
from textblob import TextBlob

def handle(req):
    blob = TextBlob(req)
    res = {
        "polarity": 0,
        "subjectivity": 0
    }

    for sentence in blob.sentences:
        res["subjectivity"] = res["subjectivity"] + sentence.sentiment.subjectivity
        res["polarity"] = res["polarity"] + sentence.sentiment.polarity

    total = len(blob.sentences)

    sentence_count = total
    polarity = res["polarity"] / total
    subjectivity = res["subjectivity"] / total

    print("Sentence Count :" + str(sentence_count))
    print("Polarity :" + str(polarity))
    print("Subjectivity :" + str(subjectivity))
