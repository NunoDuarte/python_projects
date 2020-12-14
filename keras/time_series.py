import pandas as pd
import numpy as np
# this is for jupyter-notebook %matplotlib inline
import matplotlib.pyplot as plt
from os import listdir

from keras.preprocessing import sequence
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import ModelCheckpoint

df1 = pd.read_csv("~/datasets/MovementAAL/dataset/MovementAAL_RSS_1.csv")
df2 = pd.read_csv("~/datasets/MovementAAL/dataset/MovementAAL_RSS_2.csv")

#print(df1.head())
#print(df2.head())
#print(df1.shape, df2.shape)

# store and read the dataset
path = "~/datasets/MovementAAL/dataset/MovementAAL_RSS_"
sequences = list()
for i in range(1,315):
    file_path = path + str(i) + '.csv'
    print(file_path)
    df = pd.read_csv(file_path, header=0)
    values = df.values
    sequences.append(values)



