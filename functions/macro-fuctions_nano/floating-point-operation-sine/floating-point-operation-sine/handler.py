import time as t
from math import sin, pi


def handle(req):
    """This function will calculate sine(360) multiple times"""
    startTime = t.time()
    for i in range(100001):
        for x in range(361):
            result = sin(x*pi/180)
    endTime = t.time()
    elaspedFunTime = "Total time to execute the function is: " + str(endTime-startTime) + " seconds"

    return elaspedFunTime

