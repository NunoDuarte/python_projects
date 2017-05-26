import numpy as np
import matplotlib.pyplot as plt
import PIL
import time
from PIL import Image

def threshold(imageArray):
    balanceAr = []
    newAr = imageArray
    
    for eachRow in imageArray:
        for eachPix in eachRow:
            print (eachPix) 
            
            time.sleep(5)
            
i1 = Image.open('images/numbers/0.1.png')
iar1 = np.array(i1)       

i2 = Image.open('images/numbers/y0.4.png')
iar2 = np.array(i2)  
        
i3 = Image.open('images/numbers/y0.5.png')
iar3 = np.array(i3)          

i4 = Image.open('images/sentdex.png')
iar4 = np.array(i4)          

fig = plt.figure()
ax1 = plt.subplot2grid((8,6), (0,0), rowspan=4, colspan=3)
ax2 = plt.subplot2grid((8,6), (4,0), rowspan=4, colspan=3)
ax3 = plt.subplot2grid((8,6), (0,3), rowspan=4, colspan=3)
ax4 = plt.subplot2grid((8,6), (4,3), rowspan=4, colspan=3)

ax1.imshow(iar1)
ax2.imshow(iar2)
ax3.imshow(iar3)
ax4.imshow(iar4)

plt.show()


     
            
            