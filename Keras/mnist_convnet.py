from keras import layers 
from keras import models
from keras.datasets import mnist
from keras.utils import to_categorical

# build the CNN
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu')) 
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten()) # 64*3*3 = 576
model.add(layers.Dense(64, activation='relu')) 
model.add(layers.Dense(10, activation='softmax')) # 10 output of classification

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()


