import numpy as np
import matplotlib
import PIL
from PIL import Image

i = Image.open('images/dot.png')
# image array -> convert to a np.array (3D array)
iar = np.array(i)

print (iar)

# first group of numbers is the first row. and the first line is the first pixel (4 numbers to define the pixel)
#(RGB + alpha) the alpha is for transparency
# big alpha means that it is very opaque (small transparency)



