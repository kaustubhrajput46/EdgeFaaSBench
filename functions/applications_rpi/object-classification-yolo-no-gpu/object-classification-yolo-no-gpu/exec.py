import time as t
import random
import os

startTime=t.time()
newDir = os.getcwd() + '/data/jpgs'
myList = os.listdir(newDir)
os.system("./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/jpgs/" + random.choices(myList)[0])
endTime=t.time()
print("The function has executed successfully in {:.2f} seconds.".format(endTime-startTime))