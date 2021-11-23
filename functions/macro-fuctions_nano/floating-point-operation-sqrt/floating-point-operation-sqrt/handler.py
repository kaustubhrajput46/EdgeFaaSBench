import time as t
from math import sqrt, pi

def handle(req):
    """ This function will calculate sqaure root of 1000000 numbers multiple times"""
    startTime = t.time()
    for i in range(1001):
        for x in range(1000000):
            result = sqrt(x)
    endTime = t.time()
    elapsedTime = "Total time to execute the function is: " + str(endTime-startTime) + " seconds"

    return elapsedTime

