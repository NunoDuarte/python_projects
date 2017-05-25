import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image

i = Image.open('images/numbers/y0.5.png')
# image array -> convert to a np.array (3D array)
iar = np.array(i)

plt.imshow(iar)
print(iar)
plt.show()

# first group of numbers is the first row. and the first line is the first pixel (4 numbers to define the pixel)
#(RGB + alpha) the alpha is for transparency
# big alpha means that it is very opaque (small transparency)



