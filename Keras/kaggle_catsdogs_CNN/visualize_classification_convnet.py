# Class Activation Map (CAM)
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from tensorflow.keras import models
from keras import backend as K  # perform gradient descent
from keras.applications.vgg16 import preprocess_input, decode_predictions
import tensorflow as tf
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

model = VGG16(weights='imagenet')

img_path = '/home/nuno/code/python_projects/Keras/kaggle_catsdogs_CNN/creative_commons_elephant.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = np.array(img)
x = np.expand_dims(x, axis=0)
# without color normalization prediction drops from 91.5% to 70%
x = preprocess_input(x)

preds = model.predict(x)
print('Predicted:', decode_predictions(preds, top=3)[0])

# check the region of the image used for classification
african_elephant_output = model.output[:, 386]

last_conv_layer = model.get_layer('block5_conv3')

heatmap_model = models.Model([model.inputs], [last_conv_layer.output, model.output])

# Get gradient of the winner class w.r.t. the output of the (last) conv. layer
with tf.GradientTape() as gtape:
    conv_output, predictions = heatmap_model(x)
    loss = predictions[:, np.argmax(predictions[0])]
    grads = gtape.gradient(loss, conv_output)
    pooled_grads = K.mean(grads, axis=(0, 1, 2))

# show Heatmap of CAM
heatmap = np.mean(tf.multiply(pooled_grads, conv_output), axis=-1)
heatmap = np.maximum(heatmap,0)
heatmap /= np.max(heatmap)
plt.matshow(heatmap[0], cmap='jet')
#plt.show()

## superimpose on image
# scipy interpolation to rescale the heatmap to the size of the img
# 224x224 - 14x14 = Resample by a factor of 16
heatmap = scipy.ndimage.zoom(heatmap[0], 16, order=1)
heatmap = np.uint8(255 * heatmap) # convert to RGB

plt.figure()
plt.subplot(1,2,1)
plt.imshow(img, 'gray', interpolation='none')
plt.subplot(1,2,2)
plt.imshow(heatmap,'jet', interpolation='none', alpha=0.7)
plt.imshow(img, interpolation='none',alpha=0.5)
plt.show()


