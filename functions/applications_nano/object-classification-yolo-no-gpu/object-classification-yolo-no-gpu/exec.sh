#!/bin/bash

# My first script

echo "Hello World!"

cd darknet
./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/dog.jpg

