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
    #print(file_path)
    df = pd.read_csv(file_path, header=0)
    values = df.values
    sequences.append(values)

targets = pd.read_csv("~/datasets/MovementAAL/dataset/MovementAAL_target.csv")
targets = targets.values[:,1]

# print the first sequence of the dataset (4 sensors over the duration of the action)
#print(sequences[0])

groups = pd.read_csv("~/datasets/MovementAAL/groups/MovementAAL_DatasetGroup.csv", header=0)
groups = groups.values[:,1]

# normalize data
len_sequences = []
for one_seq in sequences:
    len_sequences.append(len(one_seq))
print(pd.Series(len_sequences).describe())

#Padding the sequence with the values in last row to max length
to_pad = 129
new_seq = []
for one_seq in sequences:
    len_one_seq = len(one_seq)
    last_val = one_seq[-1]
    n = to_pad - len_one_seq
   
    to_concat = np.repeat(one_seq[-1], n).reshape(4, n).transpose()
    new_one_seq = np.concatenate([one_seq, to_concat])
    new_seq.append(new_one_seq)
final_seq = np.stack(new_seq)

#truncate the sequence to length 60
from keras.preprocessing import sequence
seq_len = 60
final_seq=sequence.pad_sequences(final_seq, maxlen=seq_len, padding='post', dtype='float', truncating='post')


