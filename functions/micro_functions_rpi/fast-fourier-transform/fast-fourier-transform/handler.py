import numpy as np
import time as t

def handle(req):
    x = np.random.rand(10000000)
    startTime = t.time()
    for i in range(9000001):
        y = np.fft.fft
    endTime = t.time()
    
    return "The function has executed successfully in {:.2f} seconds.".format(endTime-startTime)