import random
import os

NewDir = os.getcwd() + '/data/jpgs'
mylist = os.listdir(NewDir)
os.system("./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/jpgs/" + random.choices(mylist)[0])
