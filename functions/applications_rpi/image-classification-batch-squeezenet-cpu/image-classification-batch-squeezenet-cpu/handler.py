import torch
import torchvision
import urllib
from PIL import Image
from torchvision import transforms
import time as t
import random
import os

def handle(req):
    print("Executing image-classification-batch-squeezenet-cpu....")
    startTime = t.time()
    model = torch.hub.load('pytorch/vision:v0.6.0', 'squeezenet1_0', pretrained = True)

    #Test model.eval.cuda() as well
    model.eval()
    print(t.time()-startTime,",","Time for setting model in evaluation mode")

#    newDir = os.getcwd() + '/data/Imgs/'
    newDir = os.getcwd() + '/data/jpgs2/'

    myList = os.listdir(newDir)

    inferTime = t.time()

    for fileName in myList:
#        print(fileName)
#    fileName = random.choices(myList)[0]
#        print(fileName) #remove
        filePath = newDir + str(fileName)

        input_image = Image.open(filePath)
        preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # Create mini batch as expected by model

    # put the model in the eval mode
#        model.eval()
    # carryinig out the inference
        out = model(input_batch)
#        print("output shape:", out.shape)

        with open('imagenet_classes.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0]*100
#        print(classes[index[0]], percentage[index[0]].item())
#    endTime=t.time()

        _, indices = torch.sort(out, descending=True)
        [(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]
    endTime=t.time()
    print(inferTime-startTime, ",", "Load time", ",",endTime-inferTime, ",", "Infer time", ",", endTime-startTime,",", "Total time")
#    print(endTime-startTime)
    return "Function executed in {:.2f} seconds.".format(endTime-startTime)
