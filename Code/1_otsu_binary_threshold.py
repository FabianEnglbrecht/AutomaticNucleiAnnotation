import cv2
import numpy as np
import os


# Declare path and filetype of cell microscopy images
items = os.listdir("Frames")
newlist = []
for names in items:
    if names.endswith(".png"):
        newlist.append(names)
b = len(newlist)
print(b)
a = 1


# Apply otsu binary thresholding to image dataset
while a <= b:
    image_path = "Frames/frame"+str(a)+".png"
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Adjust opencv hyperparameters such as kernel size
    blur = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (9, 9), 0)
    mask_otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    kernel = np.ones((4, 4), np.uint8)
    display_image = image.copy()

    display_image[mask_otsu != 0] = (255, 255, 255)
    cv2.imwrite("./Otsu/frame"+str(a)+"_otsu.png", display_image)
    a += 1


