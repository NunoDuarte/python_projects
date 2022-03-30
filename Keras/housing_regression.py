from keras.datasets import boston_housing
from keras import models
from keras import layers
import numpy as np    
import matplotlib 
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()

# there are variables with varying dimensions. So we need to do 
# feature-wise normalization
# remove mean and divide by standard deviation
mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

# You should never use in your workflow any quantity computed on the test data, even for something as simple as data normalization.
test_data -= mean
test_data /= std

def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
# output layer with no activation function because we want a linear output
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

# perform K-cross validation
k = 4
num_val_samples = len(train_data) // k
num_epochs = 100
all_scores = []
all_mae_histories = []

for i in range(k):
    print('processing fold #', i)
    # take the validation set
    val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples] 
    val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

    # the training set is the rest of the dataset
    partial_train_data = np.concatenate( 
            [train_data[:i * num_val_samples],
            train_data[(i + 1) * num_val_samples:]], axis=0)
    partial_train_targets = np.concatenate( 
            [train_targets[:i * num_val_samples],
            train_targets[(i + 1) * num_val_samples:]], axis=0)

    model = build_model()
    NN = model.fit(partial_train_data, partial_train_targets,
            epochs=num_epochs, batch_size=1, verbose=0)
    val_mse, val_mae = model.evaluate(val_data, val_targets, verbose=0)
    all_scores.append(val_mae)

    mae_history = NN.history['mae']
    all_mae_histories.append(mae_history)

average_mae_history = [
        np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()



