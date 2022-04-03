from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt


model = load_model('models/cats_and_dogs_small_2.h5')
#model.summary()

img_path = '/home/nuno/datasets/dogs-vs-cats/cats_and_dogs_small/test/cats/cat.1700.jpg'

img = image.load_img(img_path, target_size=(150, 150)) 
img_tensor = np.array(img)
img_tensor = np.expand_dims(img_tensor, axis=0) 

plt.imshow(img_tensor[0])
plt.show()

