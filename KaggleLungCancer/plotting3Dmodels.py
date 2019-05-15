import matplotlib.pyplot as plt 
import cv2
import numpy as np
import math  
import os
import pandas as pd  
import dicom

IMG_PX_SLICE = 150
HM_SLICES = 20

data_dir = '/Volumes/LaCie02/NUNO/stage1/'
patients = os.listdir(data_dir)
labels_df = pd.read_csv('/Users/Nuno/Downloads/data_sets/stage1_labels.csv', index_col=0)

def chunks(l, n):
    '''Yield successive n-sized chunks from l'''
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def mean(l):
    return sum(l)/len(l)
        
for patient in patients[:1]:
    try:
        label = labels_df.get_value(patient, 'cancer')
        path = data_dir + patient
        slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
        slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
         
        new_slices = []
         
        slices = [cv2.resize(np.array(each_slice.pixel_array), (IMG_PX_SLICE, IMG_PX_SLICE)) for each_slice in slices]
         
        chunk_sizes = math.ceil(len(slices) / HM_SLICES)
         
        for slice_chunk in chunks(slices, chunk_sizes):
            slice_chunk = list(map(mean, zip(*slice_chunk)))
            new_slices.append(slice_chunk)
             
         
        if len(new_slices) == HM_SLICES-1:
            new_slices.append(new_slices[-1]) 
             
        if len(new_slices) == HM_SLICES-2: #if it is 18 then you should remove the last two slices
            new_slices.append(new_slices[-1]) 
            new_slices.append(new_slices[-1]) 
             
        if len(new_slices) == HM_SLICES+1: # to remove the chunks with 21 slices
            new_val = list(map(mean, zip(*[new_slices[HM_SLICES-1], new_slices[HM_SLICES]])))
            del new_slices[HM_SLICES]
            new_slices[HM_SLICES-1] = new_val
             
        if len(new_slices) == HM_SLICES+2: # remove the chunks with 22 slices
            new_val = list(map(mean, zip(*[new_slices[HM_SLICES-1], new_slices[HM_SLICES]])))
            del new_slices[HM_SLICES]
            new_slices[HM_SLICES-1] = new_val
             
        #print(len(new_slices)) # to check that all chunks have 20 slices
             
                                            
        fig = plt.figure()
        for num, each_slice in enumerate(new_slices):
            y = fig.add_subplot(4,5, num+1)
            #new_image = cv2.resize(np.array(each_slice.pixel_array), (IMG_PX_SLICE, IMG_PX_SLICE))
            y.imshow(new_slices[num])
        plt.show()
    except Exception as e:
        # again, some patients are not labeled, but JIC we still want the error if something
        # else is wrong with our code
        print(str(e))
    
    
    
    