import time as t
from math import sqrt, pi

def handle(req):
    """ This function will calculate sqaure root of 1000000 numbers multiple times"""
    startTime = t.time()
    for i in range(1001):
        for x in range(30000):
            result = sqrt(x)
    endTime = t.time()

    return "The function has executed successfully in {:.2f} seconds.".format(endTime-startTime)