# Import required Image library
from PIL import Image
import time as t
import os

def handle(req):
    startTime = t.time()
    dirName = os.path.join(os.getcwd(), "Images/Imgs")
    # reading every image from the directory
    for fileName in os.listdir(dirName):
        im = Image.open(str(dirName+'/'+fileName))
        resized_im = im.resize((400, 400))
        resized_im.save(r'ResizeImg'+'/'+'resized_'+fileName)
    endTime = t.time()

    return "The function has executed successfully in {:.2f} seconds.".format(endTime-startTime)