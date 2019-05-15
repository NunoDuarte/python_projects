import tensorflow as tf
import tqdm
import tflearn
import cv2
import numpy as np
import os
from random import shuffle
# for professional looping
from tqdm import tqdm

TRAIN_DIR = '/Users/Nuno/Downloads/train'
TEST_DIR = '/Users/Nuno/Downloads/test1'
IMG_SIZE = 50 # 50by50
# however not all pictures are 50by5o so we are going to resize them
LR = 1e-3 # Learning Rate

MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic-video')

#[catness, dogness] = [1, 0], [0, 1]
def label_img(img):
    # e.g. dog.93.png 
    # splitting by period
    # [-1] = png
    # [-2] = 93
    # [-3] = dog
    word_label = img.split('.')[-3]
    if word_label == 'cat': return [1, 0]
    elif word_label == 'dog': return [0, 1]
    
# just train once, unless you want to change the image size
def create_train_data():
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):
        label = label_img(img)
        path = os.path.join(TRAIN_DIR, img)
        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (IMG_SIZE, IMG_SIZE))
        training_data.append([np.array(img), np.array(label)])
    shuffle(training_data)
    np.save('train_data.npy', training_data)
    return training_data

def process_test_data():
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR, img)
        img_num = img.split('.')[-2]
        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (IMG_SIZE, IMG_SIZE))
        testing_data.append([np.array(img), img_num])               
    np.save('test_data.npy', testing_data)
    return testing_data

train_data = create_train_data()

    











