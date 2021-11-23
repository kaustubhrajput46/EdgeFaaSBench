import sys
import json
import nltk
import time as t
nltk.download('punkt')
from textblob import TextBlob

def handle(req):
    startTime=t.time()
    blob = TextBlob(req)
    res = {
        "polarity": 0,
        "subjectivity": 0
    }

    for sentence in blob.sentences:
        res["subjectivity"] = res["subjectivity"] + sentence.sentiment.subjectivity
        res["polarity"] = res["polarity"] + sentence.sentiment.polarity

    total = len(blob.sentences)

    res["sentence_count"] = total
    res["polarity"] = res["polarity"] / total
    res["subjectivity"] = res["subjectivity"] / total

    print(json.dumps(res))
    endTime=t.time()
    print("The function has executed successfully in {:.2f} seconds.".format(endTime-startTime))