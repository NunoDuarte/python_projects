import os
from glob import glob
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Input, Conv2D, Flatten, Dense, Conv2DTranspose, Reshape, Lambda, Activation, BatchNormalization, LeakyReLU, Dropout
from keras.models import Model
from keras import backend as K
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint 
from keras.utils import plot_model
from keras import models
import tensorflow as tf 

# Trying to train network on Multi-GPU system
strategy = tf.distribute.MirroredStrategy()
print("Number of devices: {}".format(strategy.num_replicas_in_sync))
input()

WEIGHTS_FOLDER = './weights/'
DATA_FOLDER = '/home/nuno/datasets/celeba/img_align_celeba/'

if not os.path.exists(WEIGHTS_FOLDER):
  os.makedirs(os.path.join(WEIGHTS_FOLDER,"AE"))
  os.makedirs(os.path.join(WEIGHTS_FOLDER,"VAE"))

# load data
filenames = np.array(glob(os.path.join(DATA_FOLDER, '*/*.jpg')))
NUM_IMAGES = len(filenames)
print("Total number of images : " + str(NUM_IMAGES))
# prints : Total number of images : 202599

INPUT_DIM = (128,128,3) # Image dimension
BATCH_SIZE = 512
Z_DIM = 200 # Dimension of the latent vector (z)

data_flow = ImageDataGenerator(rescale=1./255).flow_from_directory(DATA_FOLDER,
        target_size = INPUT_DIM[:2], batch_size = BATCH_SIZE, shuffle = True, class_mode = 'input', subset = 'training')

# build encoder
def build_encoder(input_dim, output_dim, conv_filters, conv_kernel_size,
                  conv_strides):
  global K
  K.clear_session()
  n_layers = len(conv_filters)

  encoder_input = Input(shape = input_dim, name = 'encoder_input')
  x = encoder_input

  for i in range(n_layers):
      x = Conv2D(filters = conv_filters[i],
                  kernel_size = conv_kernel_size[i],
                  strides = conv_strides[i],
                  padding = 'same',
                  name = 'encoder_conv_' + str(i)
                  )(x)

      x = LeakyReLU()(x)
  
  shape_before_flattening = K.int_shape(x)[1:]
  x = Flatten()(x)

  encoder_output = Dense(output_dim, name = 'encoder_output')(x)

  return encoder_input, encoder_output, shape_before_flattening, Model(encoder_input, encoder_output)

encoder_input, encoder_output, shape_before_flattening, encoder = build_encoder(input_dim = INPUT_DIM, output_dim = Z_DIM, conv_filters = [32, 64, 64, 64], conv_kernel_size = [3,3,3,3], conv_strides = [2,2,2,2])

# Decoder
def build_decoder(input_dim, shape_before_flattening, conv_filters, conv_kernel_size, 
                  conv_strides):

  n_layers = len(conv_filters)

  decoder_input = Input(shape = (input_dim,) , name = 'decoder_input')

  x = Dense(np.prod(shape_before_flattening))(decoder_input)
  x = Reshape(shape_before_flattening)(x)

  for i in range(n_layers):
      x = Conv2DTranspose(filters = conv_filters[i], 
                  kernel_size = conv_kernel_size[i],
                  strides = conv_strides[i], 
                  padding = 'same',
                  name = 'decoder_conv_' + str(i)
                  )(x)
      
      # Adding a sigmoid layer at the end to restrict the outputs 
      # between 0 and 1
      if i < n_layers - 1:
        x = LeakyReLU()(x)
      else:
        x = Activation('sigmoid')(x)

  decoder_output = x

  return decoder_input, decoder_output, Model(decoder_input, decoder_output)

decoder_input, decoder_output, decoder = build_decoder(input_dim = Z_DIM, shape_before_flattening = shape_before_flattening, conv_filters = [64,64,32,3], conv_kernel_size = [3,3,3,3], conv_strides = [2,2,2,2] )

def r_loss(y_true, y_pred):
    return K.mean(K.square(y_true - y_pred), axis = [1,2,3])

simple_autoencoder_input = encoder_input
simple_autoencoder_output = decoder(encoder_output)
simple_autoencoder = Model(simple_autoencoder_input, simple_autoencoder_output)
simple_autoencoder.summary()

# training 
LEARNING_RATE = 0.0005
N_EPOCHS = 10

optimizer = Adam(lr = LEARNING_RATE)

simple_autoencoder.compile(optimizer=optimizer, loss = r_loss)

checkpoint_ae = ModelCheckpoint(os.path.join(WEIGHTS_FOLDER, 'AE/weights.h5'), save_weights_only = True, verbose=1)

#simple_autoencoder.fit(data_flow,
#                                 shuffle=True,
#                                 epochs = N_EPOCHS,
#                                 initial_epoch = 0,
#                                 steps_per_epoch=NUM_IMAGES / BATCH_SIZE,
#                                 callbacks=[checkpoint_ae])


simple_autoencoder.load_weights('./weights/AE/weights.h5')

# Reconstruction
import matplotlib.pyplot as plt

example_batch = next(data_flow)
example_batch = example_batch[0]
example_images = example_batch[:10]

def plot_compare(images=None, add_noise=False):

  if images is None:
    example_batch = next(data_flow)
    example_batch = example_batch[0]
    images = example_batch[:10]

  n_to_show = images.shape[0]

  if add_noise:
    encodings = encoder.predict(images)
    encodings += np.random.normal(0.0, 1.0, size = (n_to_show,200))
    reconst_images = decoder.predict(encodings)

  else:
    reconst_images = simple_autoencoder.predict(images)

  fig = plt.figure(figsize=(15, 3))
  fig.subplots_adjust(hspace=0.4, wspace=0.4)

  for i in range(n_to_show):
      img = images[i].squeeze()
      sub = fig.add_subplot(2, n_to_show, i+1)
      sub.axis('off')
      sub.imshow(img)

  for i in range(n_to_show):
      img = reconst_images[i].squeeze()
      sub = fig.add_subplot(2, n_to_show, i+n_to_show+1)
      sub.axis('off')
      sub.imshow(img)
  plt.show()

plot_compare(example_images)



