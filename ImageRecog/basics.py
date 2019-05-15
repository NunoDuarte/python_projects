import numpy as np
import matplotlib.pyplot as plt
import PIL
import time
from PIL import Image
from collections import Counter

def createExamples():
    numberArrayExamples = open('numArEx.txt', 'a')
    numbersWeHave = range(0,10)
    versionsWeHave = range(1,10)
    
    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            print( str(eachNum) + '.' + str(eachVer))
            imgFilePath = 'images/numbers/' + str(eachNum) + '.' + str(eachVer) + '.png'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            eiar1 = str(eiar.tolist())
            
            lineToWrite = str(eachNum) + '::' + eiar1 + '\n'
            numberArrayExamples.write(lineToWrite)

def threshold(imageArray):
    balanceAr = []
    newAr = imageArray
    
    for eachRow in imageArray:
        for eachPix in eachRow:
            print (eachPix) 
            
            time.sleep(5)
       
def whatNumIsThis(filepath):
    matchedAr = []
    loadExamps = open('numArEx.txt', 'r').read()
    loadExamps = loadExamps.split('\n')
    
    i = Image.open(filepath)
    iar = np.array(i)
    iarl = iar.tolist()
    
    inQuestion = str(iarl)
    
    for eachExample in loadExamps:
        if len(eachExample) > 3:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            
            # each pixel in the example
            eachPixEx = currentAr.split('],')
            
            #each pixel in question
            eachPixInQ = inQuestion.split('],')
            
            x = 0
            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))
                    
                x += 1
                
    print(matchedAr)
    # what Counter does is that it tells you in a list how many times the numbers in an array appear
    y = Counter(matchedAr)
    print(y)
    
    
    graphX = []
    graphY = []
    
    for eachThing in y:
        print (eachThing)
        graphX.append(eachThing)
        print (y[eachThing])
        graphY.append(y[eachThing])
        
    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4),(1,0), rowspan=3, colspan=4)
    
    ax1.imshow(iar)
    ax2.bar(graphX,graphY, align = 'center')
    plt.ylim(900) # to cut out the minimum value to show in the plot
    
    plt.show()

            
# you can edit the test.png on Paint 2 (macOS) and draw whatever number you want and see what is the most probable number
# the trained pictures were 8by8 but the test.png is 10by8 (still words though)
# you need to draw a number between pixels 1 and 5 in horizontal and vertical axis to work properly
whatNumIsThis('images/test.png')    
    
            
# i1 = Image.open('images/numbers/0.1.png')
# iar1 = np.array(i1)       
# 
# i2 = Image.open('images/numbers/y0.4.png')
# iar2 = np.array(i2)  
#         
# i3 = Image.open('images/numbers/y0.5.png')
# iar3 = np.array(i3)          
# 
# i4 = Image.open('images/sentdex.png')
# iar4 = np.array(i4)     
  

# fig = plt.figure()
# ax1 = plt.subplot2grid((8,6), (0,0), rowspan=4, colspan=3)
# ax2 = plt.subplot2grid((8,6), (4,0), rowspan=4, colspan=3)
# ax3 = plt.subplot2grid((8,6), (0,3), rowspan=4, colspan=3)
# ax4 = plt.subplot2grid((8,6), (4,3), rowspan=4, colspan=3)
# 
# ax1.imshow(iar1)
# ax2.imshow(iar2)
# ax3.imshow(iar3)
# ax4.imshow(iar4)
# 
# plt.show()




     
            
            