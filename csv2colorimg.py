#!/usr/bin/env python3

'''
convert csv to normalzied color imgae(.png)
usage:
./csv2colorimg <input.csv> <output_directory>
'''

import os
import sys
import csv
import numpy as np
from PIL import Image
from matplotlib import cm

if __name__ == "__main__":
    input = sys.argv[1]
    output_dir = sys.argv[2]
    extension = '.png'
    output_name = os.path.splitext(os.path.basename(input))[0]
    
    input_file = open(input, 'r')
    reader = csv.reader(input_file)
    
    data = []
    for row in reader:
        data.append([float(pixel) for pixel in row])

    data = np.asarray(data)

    normalized_data = (data - np.amin(data)) / (np.amax(data) - np.amin(data))
    
    img_thermal = Image.fromarray(np.uint8(cm.inferno(normalized_data) * 255))

    img_thermal.save(output_dir+output_name+extension)