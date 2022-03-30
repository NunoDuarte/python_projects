import numpy as np
from keras.datasets import imdb
from keras import models
from keras import layers
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt 

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(
    num_words=10000)

# print one review 'integer' sequence and the output of review (1-good,0-bad)
#print(train_data[0])
#print(train_labels[0])

# get words associated with integers
word_index = imdb.get_word_index() 
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])
# it -3 because 0 - "padding", 1 - "start of sequence", 2 - "unknown"

# print one review sequence
#print(decoded_review)

# to feed our data into the network we convert our list into a tensor
# we choose one-hot encode which convert the list into a vector of 1s and 0s
def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

# prepare input data
x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)
# and output data
y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

# the network (fully connected Network)

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

# adding a validation set
x_val = x_train[:10000]
partial_x_train = x_train[10000:]
y_val = y_train[:10000]
partial_y_train = y_train[10000:]


history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(x_val, y_val))

# plot the results
history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

epochs = range(1, 20  + 1)

plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

