import torch
import torchvision
import urllib
from PIL import Image
from torchvision import transforms
import time as t
import random
import os

def handle(req):
    model = torch.hub.load('pytorch/vision:v0.6.0', 'alexnet', pretrained = True)

    newDir = os.getcwd() + '/data/jpgs/'
    myList = os.listdir(newDir)
    fileName = random.choices(myList)[0]
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
    model.eval()
    # carryinig out the inference
    out = model(input_batch)
    print("output shape:", out.shape)

    with open('imagenet_classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]

    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0]*100
    print(classes[index[0]], percentage[index[0]].item())

    _, indices = torch.sort(out, descending=True)
    [(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]

    return "The function has executed successfully."
