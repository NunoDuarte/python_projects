from keras import layers 
from keras import models
from keras.datasets import mnist
from keras.utils import to_categorical

# build the CNN
model = models.Sequential()
# 3 by 3 conv layers (filter) that go over the whole 28x28 pixel image - the output is a 26x26 grid of values
# 32 filters gives 32 features (filters) for the 28x28 pixel image
# input is 28x28x1 because it is in black and white; rgb is 28x28x3
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
# downsampling by taking the max value of each channel in a 2x2 window
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu')) 
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten()) # 64*3*3 = 576
model.add(layers.Dense(64, activation='relu')) 
model.add(layers.Dense(10, activation='softmax')) # 10 output of classification

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1)) # change to vector of 2D images
train_images = train_images.astype('float32') / 255  # normalize pixel to 0-1
test_images = test_images.reshape((10000, 28, 28, 1)) 
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# choose optimizer, loss function, and accuracy metric to evaluate CNN
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# train
model.fit(train_images, train_labels, epochs=5, batch_size=64)

# test
test_loss, test_acc = model.evaluate(test_images, test_labels)

print(test_acc)


