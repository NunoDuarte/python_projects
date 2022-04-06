#!/usr/bin/env python
# coding: utf-8

# #  Pre-process the Data - offline since we don't have much data (1500 samples - 50v50v20)

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

IMG_PX = 50     # Image pixels
HM_SLICES = 20  # How many slices


def chunks(l, n):
    """Yield successive n-size chunks from l"""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def mean(l):
    return sum(l)/len(l)
    

def process_data(patient, labels_df, img_px_size=50, hm_slices=20, visualize=False):
    label = labels_df.get_value(patient, 'cancer') # the label of cancer/no cancer for one patient
    path = data_dir + patient
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    # sorting the slices in the proper order
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2])) 
    
    new_slices = []
    # resize all slices inside slices
    slices = [cv2.resize(np.array(each_slice.pixel_array), (IMG_PX, IMG_PX)) for each_slice in slices]
    
    # size of the chunk which will be length of slices divide by HM_SLICES
    chunk_size = math.ceil(len(slices) / HM_SLICES)
    
    # this is averaging the slice_chunk in order to transform into one slice
    # and then adding all average slices to the new_slices
    # making new_slices a new image of the patient lungs (smaller data - 
    # more averaging - but now all will have the same size)
    for slice_chunk in chunks(slices, chunk_size):
        slice_chunk = list(map(mean, zip(*slice_chunk)))
        new_slices.append(slice_chunk)

    ## for all the cases that we don't get 20 slices
    # repeat the last one if there are 19
    if len(new_slices) == HM_SLICES - 1:
        new_slices.append(new_slices[-1])
    
    # repeat the last one two time if there are 18
    if len(new_slices) == HM_SLICES - 2:
        new_slices.append(new_slices[-1])
        new_slices.append(new_slices[-1])
    
    # there are 22; the final 2 slices we are going to average them together
    if len(new_slices) == HM_SLICES + 2:
        new_val = list(map(mean, zip(*[new_slices[HM_SLICES-1], new_slices[HM_SLICES]])))
        # delete the last slice and add the new avergare of the last two
        # as the new last slice
        del new_slices[HM_SLICES]
        new_slices[HM_SLICES-1] = new_val
                                       
    # do the same thing as in the 22 cases
    if len(new_slices) == HM_SLICES + 1:
        new_val = list(map(mean, zip(*[new_slices[HM_SLICES-1], new_slices[HM_SLICES]])))
        # delete the last slice and add the new avergare of the last two
        # as the new last slice
        del new_slices[HM_SLICES]
        new_slices[HM_SLICES-1] = new_val
        
    if visualize:    
        fig = plt.figure()
        for num, each_slice in enumerate(new_slices):
            y = fig.add_subplot(4,5, num+1)
            y.imshow(each_slice)

        plt.show()
        
    if label == 1: label = np.array([0,1])
    elif label == 0: label = np.array([1,0])
    
    return np.array(new_slices), label

much_data = []

for num, patient in enumerate(patients):
    # check where we are
    if num%100==0:
        print(num)
        
    
    try: 
        img_data, label = process_data(patient, labels_df, img_px_size=IMG_PX, hm_slices=HM_SLICES)
        much_data.append([img_data, label])
    except KeyError as e:
        print('This is unlabeled data')
        

np.save('muchdata-{}-{}-{}.npy'.format(IMG_PX, IMG_PX, HM_SLICES), much_data)
    

