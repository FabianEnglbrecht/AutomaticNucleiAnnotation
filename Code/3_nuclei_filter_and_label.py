import cv2
import statistics
from skimage import data, measure, io, img_as_ubyte
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb, rgb2gray
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Declare path and filetype of background images
items = os.listdir("./12_Black")
newlist = []
for names in items:
    if names.endswith("black.png"):
        newlist.append(names)
b = len(newlist)
print(b)
a = 1


while a <= b:
    # Apply watershed segmentation to binary thresholded images
    image_path = "./Otsu/frame"+str(a)+"_otsu.png"
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(3))
    cleared = clear_border(bw)
    label_image = label(cleared)
    image_label_overlay = label2rgb(label_image, image=image)

    # Get properties for each individual segmented object
    props = measure.regionprops_table(label_image, image, properties=['label','area','coords']) #,'equivalent_diameter','mean_intensity'
    props2 = measure.regionprops_table(label_image, image, properties=['area'])
    df = pd.DataFrame(props)
    df2 = pd.DataFrame(props2)
    flat_list = [item for sublist in df2.values.tolist() for item in sublist]


    # Calculate the median val
    def reject_outliers_2(data, m=2.):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d / (mdev if mdev else 1.)
        return data[s < m]


    data_points = np.array(flat_list)
    flat_list_2=reject_outliers_2(data_points)


    # Get +- 50% of the median area
    flat_list_4 = [i for i in flat_list_2 if i >= statistics.median(flat_list)*0.50 and i <= statistics.median(flat_list)*1.5]           
    

    # Get all objects
    #flat_list_4 = [i for i in flat_list_2]             
    

    # List with pixel values of nuclei
    list=df[df['area'].isin(flat_list_4)]['coords'].to_list()   


    # Export object properties to a .csv file
    df[df['area'].isin(flat_list_4)].filter(items=["coords"]).to_csv("test.csv")


    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)


    # Generate annotation masks onto background
    from PIL import Image
    picture = Image.open("./Black/frame"+str(a)+"_black.png")
    pixels = picture.load()

    for j in range(len(list)):
        if j % 10 == 0:
            color = (31, 119, 180)
        elif j % 10 == 1:
            color = (255, 127, 14)
        elif j % 10 == 2:
            color = (44, 160, 44)
        elif j % 10 == 3:
            color = (214, 39, 40)
        elif j % 10 == 4:
            color = (148, 103, 189)
        elif j % 10 == 5:
            color = (140, 86, 75)
        elif j % 10 == 6:
            color = (227, 119, 194)
        elif j % 10 == 7:
            color = (127, 127, 127)
        elif j % 10 == 8:
            color = (188, 189, 34)
        elif j % 10 == 9:
            color = (23, 190, 207)
        else:
            color = (255, 255, 255)
        for i in range(len(list[j])): # range and position
            pixels[int(list[j][i][1]),int(list[j][i][0])] = color


    # Preview of masks        
    #picture.show()


    # Export masks
    picture.save("./Masks/frame"+str(a)+"_mask.png")
    #picture.close()
    a += 1



