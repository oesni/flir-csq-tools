import csv
import cv2
import os

input = os.sys.argv[1]
output_dir = os.sys.argv[2]

img = cv2.imread(input, cv2.IMREAD_ANYDEPTH|cv2.IMREAD_ANYCOLOR)
height, width = img.shape

img_array = img.flatten()
img_array = img.reshape(480,640)

name = os.path.basename(input)
name = os.path.splitext(name)[0]

output_file = open(output_dir+name+'.csv', "w")
writer = csv.writer(output_file)

writer.writerows(img_array)
output_file.close()

