# Import required Image library
from PIL import Image
import os

def handle(req):
    dirName = os.path.join(os.getcwd(), "Imgs/Imgs")
#    newDir = os.path.join(os.getcwd(), "ResizeImg")

#    os.makedirs(newDir)
    # reading every image from the directory
    for fileName in os.listdir(dirName):
        im = Image.open(str(dirName+'/'+fileName))
        resized_im = im.resize((400, 400))
        resized_im.save(r'ResizeImg'+'/'+'resized_'+fileName)

#        im = Image.open(fileName)
        # using pillow we are going to resize it.
#        print("The size of the image before resizing.")
#        print("Width:%s Height:%s" % (im.size[0], im.size[1]))

        # Make the new image half the widht and half height of the original image
#        resized_im = im.resize((round(im.size[0] * 0.5)), (round(im.size[1] * 0.5))

#        print(im.size)
#        print(resized_im.size)
        # Save the cropped image
#        resized_im.save()

    return "The function of Image Resizing is executed successfully."

