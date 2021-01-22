import cv2
import numpy as np
from PIL import Image
import random
import os


# Declare path and filetype of nuclei masks
items = os.listdir("Masks")
newlist = []
for names in items:
    if names.endswith(".png"):
        newlist.append(names)
b = len(newlist)
print(b)
a = 1


while a <= b:
    # Declare path and filetype of nuclei masks
    image = cv2.imread("Masks/frame"+str(a)+"_mask.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Set threshold level for random noise
    threshold_level = 50


    # Find coordinates of all pixels below threshold
    coords = np.column_stack(np.where(gray < threshold_level))


    # Declare path and filetype of microscopy images
    picture = Image.open('Frames/frame'+str(a)+'.png')
    pixels = picture.load()


    # Add random noise to each image of the dataset
    for i in range(len(coords)): # your range and position
        pixels[int(coords[i][1]), int(coords[i][0])] = (random.randint(0, 50) , random.randint(0, 50), random.randint(0, 50))
        #pixels[int(coords[i][1]), int(coords[i][0])] = (0, 0, 0)    # no random noise added to the image


    # Export image without random noise added    
    #picture.save("Output/frame"+str(a)+"_reduced.png")


    # Export image with random noise added    
    picture.save("Output_blurred/frame" + str(a) + "_reduced.png")
    a += 1
