#!/bin/bash

cd yolo-custom
./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/dog.jpg
