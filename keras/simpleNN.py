from keras import models
from keras import layers

model = models.Sequential()

# first layer (output, input)
model.add(layers.Dense(32, input_shape=(784,)))
# second layer (only output)  - it takes the size of the input to be the same as the output of the 
# previous layer
model.add(layers.Dense(32))

# stop at section 3.4
