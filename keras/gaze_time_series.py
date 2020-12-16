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

df1 = pd.read_csv("~/datasets/gazeSeq_IST/dataset/gazeSeq-1.csv")
df2 = pd.read_csv("~/datasets/gazeSeq_IST/dataset/gazeSeq-2.csv")

#print(df1.head())
#print(df2.head())
#print(df1.shape, df2.shape)

# store and read the dataset
path = "~/datasets/gazeSeq_IST/dataset/gazeSeq-"
sequences = list()
for i in range(1,52):
    file_path = path + str(i) + '.csv'
    #print(file_path)
    df = pd.read_csv(file_path, header=0)
    values = df.values
    sequences.append(values)

targets = pd.read_csv("~/datasets/gazeSeq_IST/dataset/gazeSeq_target.csv")
targets = targets.values[:,1]

# print the first sequence of the dataset (4 sensors over the duration of the action)
#print(sequences[0])

#groups = pd.read_csv("~/datasets/MovementAAL/groups/MovementAAL_DatasetGroup.csv", header=0)
#groups = groups.values[:,1]

#truncate the sequence to length 100
from keras.preprocessing import sequence
seq_len = 100
final_seq=sequence.pad_sequences(sequences, maxlen=seq_len, padding='post', dtype='float', truncating='post')

# separate dataset between train|validation|test set
train = [final_seq[i] for i in range(0, 35)]
validation = [final_seq[i] for i in range(36, 40)]
test = [final_seq[i] for i in range(41, 51)]

train_target = [targets[i] for i in range(0, 35)]
validation_target = [targets[i] for i in range(36, 40)]
test_target = [targets[i] for i in range(41, 51)]

train = np.array(train)
validation = np.array(validation)
test = np.array(test)

train_target = np.array(train_target)
#train_target = (train_target+1)/2

validation_target = np.array(validation_target)
#validation_target = (validation_target+1)/2

test_target = np.array(test_target)
#test_target = (test_target+1)/2

## build the model
model = Sequential()
model.add(LSTM(128, input_shape=(seq_len, 1)))
model.add(Dense(1, activation='sigmoid'))

model.summary()

adam = Adam(lr=0.005)
chk = ModelCheckpoint("best_model.pkl", monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
model.fit(train, train_target, epochs=500, batch_size=32, callbacks=[chk], validation_data=(validation,validation_target))

print("Test data results")
#loading the model and checking accuracy on the test data
model = load_model("best_model.pkl")

from sklearn.metrics import accuracy_score
#test_preds = model.predict_classes(test)
test_preds = (model.predict(test) > 0.5).astype("int32")
print('test', test_target)
print('preds', test_preds)
print("accuracy score -", accuracy_score(test_target, test_preds))




