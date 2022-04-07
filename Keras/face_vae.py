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
tf.compat.v1.disable_eager_execution()

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
def build_vae_encoder(input_dim, output_dim, conv_filters, conv_kernel_size,
                  conv_strides, use_batch_norm = False, use_dropout = False):
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
      if use_batch_norm:
        x = BathcNormalization()(x)

      x = LeakyReLU()(x)

      if use_dropout:
        x = Dropout(rate=0.25)(x)


  shape_before_flattening = K.int_shape(x)[1:]
  x = Flatten()(x)

  # Part for representing multivariate standard normal distribution
  mean_mu = Dense(output_dim, name = 'mu')(x)
  log_var = Dense(output_dim, name = 'log_var')(x)

  # Defining a function for sampling
  def sampling(args):
      mean_mu, log_var = args
      epsilon = K.random_normal(shape=K.shape(mean_mu), mean=0., stddev=1.)
      return mean_mu + K.exp(log_var/2)*epsilon

  encoder_output = Lambda(sampling, name='encoder_output')([mean_mu, log_var])

  return encoder_input, encoder_output, mean_mu, log_var, shape_before_flattening, Model(encoder_input, encoder_output)

vae_encoder_input, vae_encoder_output, mean_mu, log_var, vae_shape_before_flattening, vae_encoder = build_vae_encoder(input_dim = INPUT_DIM, output_dim = Z_DIM, conv_filters = [32, 64, 64, 64], conv_kernel_size = [3,3,3,3], conv_strides = [2,2,2,2])

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

vae_decoder_input, vae_decoder_output, vae_decoder = build_decoder(input_dim = Z_DIM, shape_before_flattening = vae_shape_before_flattening, conv_filters = [64,64,32,3], conv_kernel_size = [3,3,3,3], conv_strides = [2,2,2,2] )

vae_input = vae_encoder_input
vae_output = vae_decoder(vae_encoder_output)
vae_model = Model(vae_input, vae_output)
vae_model.summary()

# training 
LEARNING_RATE = 0.0005
N_EPOCHS = 200
LOSS_FACTOR = 10000

def r_loss(y_true, y_pred):
    return K.mean(K.square(y_true - y_pred), axis = [1,2,3])

def kl_loss(y_true, y_pred):
    kl_loss =  -0.5 * K.sum(1 + log_var - K.square(mean_mu) - K.exp(log_var), axis = 1)
    return kl_loss

def total_loss(y_true, y_pred):
    return LOSS_FACTOR*r_loss(y_true, y_pred) + kl_loss(y_true, y_pred)

optimizer = Adam(lr = LEARNING_RATE)

vae_model.compile(optimizer=optimizer, loss = total_loss, metrics = [r_loss, kl_loss])

checkpoint_ae = ModelCheckpoint(os.path.join(WEIGHTS_FOLDER, 'VAE/weights.h5'), save_weights_only = True, verbose=1)

#vae_model.fit(data_flow, shuffle=True, epochs = N_EPOCHS, initial_epoch = 0,
#        steps_per_epoch=NUM_IMAGES / BATCH_SIZE, callbacks=[checkpoint_ae])


vae_model.load_weights('./weights/VAE/weights.h5')

# Reconstruction
import matplotlib.pyplot as plt

example_batch = next(data_flow)
example_batch = example_batch[0]
example_images = example_batch[:10]

def plot_compare(images):

  n_to_show = images.shape[0]

  reconst_images = vae_model.predict(images)

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



