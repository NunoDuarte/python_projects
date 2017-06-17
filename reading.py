import dicom # read dicom files
import os # do directory operations
import pandas as pd # nice for data analysis
# needed to change the python version
import matplotlib.pyplot as plt 
import cv2
import numpy as np

data_dir = '/Volumes/LaCie02/NUNO/stage1/'
patients = os.listdir(data_dir)
labels_df = pd.read_csv('/Users/Nuno/Downloads/data_sets/stage1_labels.csv', index_col=0)

labels_df.head()

for patient in patients[:10]:
    label = labels_df.get_value(patient, 'cancer')
    path = data_dir + patient
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
    print(len(slices), slices[0].pixel_array.shape)
    # every patient has a 3D image with x images of 512x512.
    # first patient has 195 images the 2nd 265, etc
    
    
IMG_PX_SLICE = 150

for patient in patients[:2]:
    label = labels_df.get_value(patient, 'cancer')
    path = data_dir + patient
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
    
    fig = plt.figure()
    for num, each_slice in enumerate(slices[:12]):
        y = fig.add_subplot(3,4, num+1)
        new_image = cv2.resize(np.array(each_slice.pixel_array), (IMG_PX_SLICE, IMG_PX_SLICE))
        y.imshow(new_image)
    plt.show()
    

import math    

HM_SLICES = 20

def chunks(l,n):
    '''Yield successive n-sized chunks from l'''
    for i in range(0, len(l), n):
        yield l[i:1 + n]
        
def mean(l):
    return sum(l)/len(l)

for patient in patients[:10]:
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
        
    print(len(new_slices))
    
    if len(new_slices) == HM_SLICES-1:
        new_slices.append(new_slices[-1]) 
        new_slices.append(new_slices[-1]) #if it is not -1 but -2
        
    if len(new_slices) == HM_SLICES+2:
        new_val = list(map(mean, zip(*[new_slices[HM_SLICES-1], new_slices[HM_SLICES]])))
        del new_slices[HM_SLICES]
        new_slices[HM_SLICES-1] = new_val
        
                                       
    
    