from math import cos,pi
import time as t

def handle(req):
    """This function will calculate the cosine(360) multiple times"""
    startTime = t.time()
    for i in range(100001):
        for x in range(361):
            result = cos(x*pi/180)
    endTime = t.time()
    return "The function has executed successfully in {:.2f} seconds.".format(endTime-startTime)